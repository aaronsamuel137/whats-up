import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.web
import unittest
import json

import app

class TestTornadoWeb(unittest.TestCase):
    response = None

    def setUp(self):
        application = tornado.web.Application([
                (r'/data', app.APIHandler),
                ])

        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(9999)

    def handle_request(self, response):
        self.response = response
        tornado.ioloop.IOLoop.instance().stop()

    def testAPIHandler(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch('http://localhost:9999/data', self.handle_request)

        tornado.ioloop.IOLoop.instance().start()

        self.failIf(self.response.error)
        # print(json.loads(self.response.body.decode('utf-8')))
        self.assertTrue('example tweet1' in str(self.response.body))

if __name__ == '__main__':
    unittest.main()
