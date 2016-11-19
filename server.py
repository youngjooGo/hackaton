import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.httpserver


from hackaton import *

settings = {'debug' : True,}

application = tornado.web.Application([
    (r'/ws', Dairy_Handler),
    ])

if __name__ == '__main__':
	Loop = tornado.ioloop.IOLoop.instance()
	#tornado.websocket.websocket_connect("ws://localhost:80")
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	Loop.start()