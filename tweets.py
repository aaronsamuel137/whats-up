from twython import Twython
from twython import TwythonStreamer
import time

appKeyFile = open("appKey.txt", "r")
APP_KEY = appKeyFile.readline().rstrip()
APP_SECRET = appKeyFile.readline().rstrip()

#twitter = Twython(APP_KEY, APP_SECRET, oauth_version=1)
#auth = twitter.get_authorized_tokens()
OAUTH_TOKEN = appKeyFile.readline().rstrip()#auth['oauth_token']
OAUTH_TOKEN_SECRET = appKeyFile.readline().rstrip()#auth['oauth_token_secret']

def get_tweets(pipe, queue):
    """This method defines a process that gets tweets from the Twitter streaming API.

    Args:
      pipe (multiprocessing.Pipe): The sending end of a Pipe object


    """
    stream = MyStreamer(pipe, queue)
    stream.statuses.sample()

class MyStreamer(TwythonStreamer):

    def on_success(self, data):
        self.pipe.send(data)
        self.q.put(data)

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        self.disconnect()

    def __init__(self, pipe, queue):
        TwythonStreamer.__init__(self, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        self.pipe = pipe
        self.q = queue


