from twython import Twython
from twython import TwythonStreamer
import time

# auth info for twitter
appKeyFile = open('appKey.txt', 'r')
APP_KEY = appKeyFile.readline().rstrip()
APP_SECRET = appKeyFile.readline().rstrip()
OAUTH_TOKEN = appKeyFile.readline().rstrip()
OAUTH_TOKEN_SECRET = appKeyFile.readline().rstrip()

# twython object for rest API calls
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=1)


def get_tweets(pipe, queue):
    """This method defines a process that gets tweets from the Twitter streaming API.

    Args:
      pipe (multiprocessing.Pipe): The sending end of a Pipe object


    """
    stream = MyStreamer(pipe, queue)
    stream.statuses.sample()

def get_tweets_by_topic(topic):
    return twitter.search(q=topic, result_type='recent', lang='en', count='100')


class MyStreamer(TwythonStreamer):
    """MyStreamer pipes the streaming twitter data to the main app."""

    def on_success(self, data):
        self.pipe.send(data)
        self.q.put(data)

    def on_error(self, status_code, data):
        print(status_code)
        print(data)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        self.disconnect()

    def __init__(self, pipe, queue):
        TwythonStreamer.__init__(self, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        self.pipe = pipe
        self.q = queue


