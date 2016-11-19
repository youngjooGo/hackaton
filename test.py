from websocket import create_connection
import base64
import json

ws = create_connection("ws://localhost:8888/ws")
imageFile = open('test.jpg','rb')
image = base64.b64encode(imageFile.read())
print "Sending 'Hello, World'..."
js = {'msg':'hello','image':image}
ws.send(js)
print "Sent"
print "Reeiving..."
result =  ws.recv()
print "Received '%s'" % result
ws.close()
