import time

def get_tweets(pipe):
    """This method defines a process that gets tweets from the Twitter streaming API."""
    num = 0
    while (True):
        tweets = ['example tweet {}'.format(str(i)) for i in range(num, num + 10)]
        pipe.send(tweets)
        num += 10
        time.sleep(5)
