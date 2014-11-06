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

print APP_KEY
print APP_SECRET
print OAUTH_TOKEN
print OAUTH_TOKEN_SECRET

samples = open("samples.txt", "w")

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            samples.write(str(data))
            samples.write("\n\n\n")

    def on_error(self, status_code, data):
        print status_code

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        self.disconnect()


stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.statuses.sample()
#time.sleep(10)
stream.disconnect()
print "Done"
