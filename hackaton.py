# -*- coding: utf-8 -*-
__author__ = 'yjGo'

import tornado.web
import tornado.websocket
import tornado.ioloop
from tornado.options import define, options
import tornado.auth
import tornado.httpclient
import tornado.escape
import tornado.gen
import random
#import MySQLdb
import json
import cStringIO
import base64
from PIL import Image



def get_dairy_list(index):
	db = MySQLdb.connect("localhost",'root','y0108009','hackaton')
	cursor = db.cursor()
	cursor.execute("select * from dairy where user_idx = %d" % index)
	data = cursor.fetchall()
	db.close()
	return data

def get_my_dairy(index):
	db = MySQLdb.connect("localhost","root",'y0108009','hackaton')
	cursor = db.cursor()
	cursor.execute("select * from dairy where c_idx = %d" % index)
	data = cursor.fetchone()
	db.close()
	return data

def get_other_dairy(index,number):
	db = MySQLdb.connect("localhost","root",'y0108009','hackaton')
	cursor = db.cursor()
	cursor.execute("select * from dairy where user_idx is not %d" % index)
	data = cursor.fetchall()
	db.close()

	#TODO random

def set_my_dairy(dairy):
	db = MySQLdb.connect("localhost","root",'y0108009','hackaton')
	cursor = db.cursor()
	cursor.execute("Insert into dairy value(%d,%d,%s,%s,%d,%s)")

def set_reply(reply):
	db = MySQLdb.connect("localhost","root",'y0108009','hackaton')
	cursor = db.cursor()

class Dairy_Handler(tornado.websocket.WebSocketHandler):
	def open(self):
		print("Websocket opened")

	def on_message(self,msg):
		print 'on message'

		js = json.loads(msg)
		image_string = cStringIO.StringIO(base64.b64decode(msg['image']))
		image = Image.open(image_string)
		image.save('out.jpg')

		if js['type'] == 'showMyList':
			#json format => {'type':'showMyList','user_idx':int}
			result = get_dairy_list(js['user_idx'])
		else if js['type'] == 'showMyDairy':
			#json format => {'type':'showMyDairy','user_idx':int,'c_idx':int}
			result = get_my_dairy(js['c_idx'])
		else if js['type'] == 'showOtherDairy':
			#json format => {'type':'showOtherDairy','user_idx':int,'number':int}
			result = get_other_dairy(js['user_idx'],js['number'])
		else if js['type'] == 'writeMyDairy':
			#json format => {'type':'wirteMyDairy','dairy':{'content:'@@','subject':int,'image':'null or imagestream'}}
			result = set_my_dairy(js['dairy'])
		else if js['type'] == 'writeReply':
			#json format => {'tyep':'writeReply','reply':{'content':'@@@',c_idx:int,is_frist:boolean}}
			result = set_reply(js['reply'])
	
		#TODO
		#self.write_message(message)

	def on_close(self):
		print "bye"





		#{'content':{'content':'dd','subject':'22','oimag'}}



