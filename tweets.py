from twython import Twython
from twython import TwythonStreamer
from multiprocessing import Queue
import time
import json
import redis

# auth info for twitter
appKeyFile = open('appKey.txt', 'r')
APP_KEY = appKeyFile.readline().rstrip()
APP_SECRET = appKeyFile.readline().rstrip()
OAUTH_TOKEN = appKeyFile.readline().rstrip()
OAUTH_TOKEN_SECRET = appKeyFile.readline().rstrip()

# twython object for rest API calls
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=1)

def get_tweets(tweet_queue, hashtag_queue):
    """
    This method defines a process that gets tweets from the Twitter streaming API.

    Args:
      pipe (multiprocessing.Pipe): The sending end of a Pipe object
      queue (multiprocessing.Queue): The object for sending the hashtag map back
    """
    stream = MyStreamer(tweet_queue, hashtag_queue)
    stream.statuses.sample() #comment out for front end testing

def get_tweets_by_topic(topic):
    return twitter.search(q=topic, result_type='recent', lang='en', count='100')

class MyStreamer(TwythonStreamer):
    """MyStreamer pipes the streaming twitter data to the main app."""

    def add_hashtags_to_map(self, data):
        if not 'entities' in data or not 'hashtags' in data['entities']:
            return

        if self.redis:
            for tag in data['entities']['hashtags']:
                if self.r_server.exists(tag['text']):
                    self.r_server.incr(tag['text'])
                else:
                    self.r_server.set(tag['text'], 1)

        else:
            for tag in data['entities']['hashtags']:
                if tag['text'] in self.hashtag_map:
                    self.hashtag_map[tag['text']] += 1
                else:
                    self.hashtag_map[tag['text']] = 1
                try:
                    self.q.get_nowait()
                except Exception as e:
                    pass
                # File of the current map for testing purposes
                #hashtagFile = open("HashtagTestingFile.txt", "w")
                #map_string = json.dumps(dict(self.hashtag_map))
                #hashtagFile.write(map_string)
                #hashtagFile.close()
                self.q.put(self.hashtag_map)

    def send_tweet(self, data):
        if self.tweet_queue.full():
            try:
                self.tweet_queue.get_nowait()
            except:
                pass
        self.tweet_queue.put(data, True, 2)

    def on_success(self, data):
        self.add_hashtags_to_map(data)
        self.send_tweet(data)

    def on_error(self, status_code, data):
        print(status_code)
        print(data)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        self.disconnect()

    def __init__(self, tweet_queue, hashtag_queue):
        TwythonStreamer.__init__(self, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        self.tweet_queue = tweet_queue
        self.q = hashtag_queue
        self.hashtag_map = {}

        self.r_server = redis.Redis('localhost')
        try:
            self.r_server.get('something') # try to use redis to see if its available
            self.redis = True
        except redis.exceptions.ConnectionError:
            print('WARNING: Redis server not running. App will run in in-memory mode')
            self.redis = False

    def prune(self):
        # Determine when it is time to cut out an entry in the map
        max_value = max(self.hashtag_map.values())
        cutoff_fraction = 0.25
        cutoff_value = max_value * cutoff_fraction

        # Remove entries where the value is too small
        keys_to_remove = []
        for key, value in self.hashtag_map.items():
            if cutoff_value > value:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.hashtag_map[key]
