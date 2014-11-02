import tornado.ioloop
import tornado.web
import os.path
import json
from tweets import get_tweets

# keep this flag true to avoid having to restart the application to reload files
DEBUG = True

# Handler for main page
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        tweets = get_tweets()
        self.render('home.html', tweets=tweets)


# Handler for our rest API
class APIHandler(tornado.web.RequestHandler):
    def get(self):
        # parse the query string to get the number of tweets to display, default is 10
        try:
            number = int(self.get_argument('number', default='10'))
        except:
            self.write('invalid query parameter')
            return
        tweets = get_tweets()
        self.write(json.dumps(tweets[:number] if len(tweets) >= number else tweets))

# handlers for every url go here
handlers = [
    (r'/', MainHandler),
    (r'/data', APIHandler),
]

# add the templates directory to application settings
settings = dict(template_path=os.path.join(os.path.dirname(__file__), 'templates'))
application = tornado.web.Application(handlers, debug=DEBUG, **settings)

# start the server
if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
