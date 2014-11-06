import tornado.ioloop
import tornado.web
import os.path
import json
import time # need for sleep, we might be able to remove this when the test get_tweet function is updated

from tweets import get_tweets
from multiprocessing import Process, Pipe
from tornado.options import parse_command_line, define, options

# optional commandline args and default values
define('port', default=8888)
define('debug', default=True)


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

# Handler for our rest API
class APIHandler(tornado.web.RequestHandler):
    def initialize(self, pipe):
        self.pipe = pipe

    def get(self):
        # parse the query string to get the number of tweets to display, default is 10
        try:
            number = int(self.get_argument('number', default='10'))
        except:
            self.write('invalid query parameter')
            return
        topic = self.get_argument('topic', default='')
        tweets = self.pipe.recv()
        self.write(json.dumps(tweets[:number] if len(tweets) >= number else tweets))

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
    parent_conn, child_conn = Pipe()

    # handlers for every url go here
    handlers = [
        (r'/', MainHandler),
        (r'/data', APIHandler, dict(pipe=parent_conn)),
        (r'/about', AboutHandler),
        (r'/sentiments', SentimentsHandler),
        (r'/trending', TrendingHandler),
    ]

    twitter_stream = Process(target=get_tweets, args=(child_conn,))
    twitter_stream.start()

    application = tornado.web.Application(handlers, debug=options.debug, **settings)
    application.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()
