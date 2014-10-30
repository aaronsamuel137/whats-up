import tornado.ioloop
import tornado.web
import os.path

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        tweets = ['example tweet'];
        self.render('home.html',
                    tweets=tweets)

handlers = [
    (r"/", MainHandler),
]

settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"))

application = tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
