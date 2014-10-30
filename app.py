import tornado.ioloop
import tornado.web
import os.path
from tweets import get_tweets

# Handler for main page
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        tweets = get_tweets()
        self.render('home.html', tweets=tweets)

# handlers for every url go here
handlers = [
    (r'/', MainHandler),
]

# add the templates directory to application settings
settings = dict(template_path=os.path.join(os.path.dirname(__file__), 'templates'))
application = tornado.web.Application(handlers, **settings)

# start the server
if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
