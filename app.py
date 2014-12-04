import tornado.ioloop
import tornado.web
import tornado.escape
import os.path
import json
import pickle
import sys
import redis

from tweets import get_tweets, get_tweets_by_topic
from tweet_classify import extract_features
from multiprocessing import Process, Pipe, Queue, Manager
from tornado.options import parse_command_line, define, options

# optional commandline args and default values
define('port', default=8888)
define('debug', default=False)

# filter out tweets with these words
stopWordsFile = open('StopWords.txt', 'r')
STOP_WORDS = [line.rstrip() for line in stopWordsFile]


# Handler for main page
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('home.html', title="What's Up")

# Handler for about page
class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('about.html', title="About")

# Handler for trending page
class TrendingHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('trending.html', title="Trending")

# Handler for sentiments page
class SentimentsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('sentiments.html', title="Sentiments")

# Handler for the live updating hashtag counts
class HashtagHandler(tornado.web.RequestHandler):
    def initialize(self, tag_queue):
        self.tag_queue = tag_queue
        self.tag_map = '{}'
        self.r_server = redis.Redis('localhost')
        try:
            self.r_server.get('something') # try to use redis to see if its available
            self.redis = True
        except redis.exceptions.ConnectionError:
            self.redis = False

    def get(self):
        try:
            if self.redis:
                list_key_value_pair = [{'tag': key.decode('utf-8'), 'count': int(self.r_server.get(key).decode('utf-8'))} for key in self.r_server.keys()]
            else:
                hashtag_dict = self.tag_queue.get(True, 2)
                list_key_value_pair = [{'tag':key,'count':value} for key,value in sorted(hashtag_dict.items(), key=lambda a:a[-1], reverse=True)]
            self.tag_map = json.dumps(list_key_value_pair)
        except:
            print(sys.exc_info()[0])
        self.write(self.tag_map)

# Handler for our rest API
class APIHandler(tornado.web.RequestHandler):
    def initialize(self, tweet_queue):
        self.tweet_queue = tweet_queue
        f = open('my_classifier.pickle', 'rb')
        self.classifier = pickle.load(f)
        f.close()

    def get(self):
        # parse the query string to get the number of tweets to display, default is 10
        try:
            number = int(self.get_argument('number', default='10'))
        except:
            self.write('invalid query parameter')
            return
        topic = self.get_argument('topic', default='')

        # use the rest API when searching by topic
        if topic != '':
            response = get_tweets_by_topic(topic)
            tweets = []
            for tweet in response['statuses']:
                if self.filter_tweet(tweet):
                    tweets.append({'text': tweet['text'], 'sentiment': self.classifier.classify(extract_features(tweet['text'])), 'rt_count': tweet['retweet_count']})
            self.write(json.dumps(tweets))
            return

        # use the streaming API when searching by in general
        tweets = []
        while len(tweets) < number:
            tweet = self.tweet_queue.get(True, 2)
            if self.filter_tweet(tweet):
                tweets.append({'text': tweet['text'], 'sentiment': self.classifier.classify(extract_features(tweet['text']))})

        self.write(json.dumps(tweets))

    def filter_tweet(self, tweet):
        if 'text' not in tweet: return False
        if 'lang' in tweet and tweet['lang'] != 'en': return False
        if 'possibly_sensitive' in tweet and tweet['possibly_sensitive'] == True: return False
        if any(word in tweet['text'] for word in STOP_WORDS): return False
        return True


# add the templates directory and static directory to application settings
settings = dict(template_path=os.path.join(os.path.dirname(__file__), 'templates'),
                static_path=os.path.join(os.path.dirname(__file__), 'static'))

# start the server
if __name__ == '__main__':
    parse_command_line()

    print('server running on port ' + str(options.port))

    if options.debug:
        print('running app in debug mode')

    # pipe for piping data from the twitter stream process
    #parent_conn, child_conn = Pipe()
    tweet_queue = Queue()
    hashtag_queue  = Queue()

    # handlers for every url go here
    handlers = [
        (r'/', MainHandler),
        (r'/data', APIHandler, dict(tweet_queue=tweet_queue)),
        (r'/about', AboutHandler),
        (r'/sentiments', SentimentsHandler),
        (r'/trending', TrendingHandler),
        (r'/hashtagmap', HashtagHandler, dict(tag_queue=hashtag_queue)),
    ]

    twitter_stream = Process(target=get_tweets, args=(tweet_queue, hashtag_queue,))
    twitter_stream.daemon = True
    twitter_stream.start()

    application = tornado.web.Application(handlers, debug=options.debug, **settings)
    application.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()
