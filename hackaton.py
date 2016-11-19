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
import MySQLdb
import json
import cStringIO
import base64
from PIL import Image



def get_dairy_list(index):
	try:
		db = MySQLdb.connect("localhost",'root','y0108009','hackaton')
		cursor = db.cursor()
		cursor.execute("select * from dairy where user_idx = %d" % index)
		data = cursor.fetchall()
		db.close()
		return data
	except Exception, e:
		return -1

def get_my_dairy(index):
	try:
		db = MySQLdb.connect("localhost","root",'y0108009','hackaton')
		cursor = db.cursor()
		cursor.execute("select * from dairy where c_idx = %d" % index)
		data = cursor.fetchone()
		db.close()
		return data
	except Exception, e:
		return -1

def get_reply(index):
	try:
		db = MySQLdb.connect("localhost","root",'y0108009','hackaton')
		cursor = db.cursor()
		cursor.execute("select * from reply where c_idx = %d" % index)
		data = cursor.fetchone()
		db.close()
		return data
	except Exception, e:
		return -1

def get_other_dairy(index,number):
	try:
		db = MySQLdb.connect("localhost","root",'y0108009','hackaton')
		cursor = db.cursor()
		cursor.execute("select * from dairy where user_idx is not %d" % index)
		data = cursor.fetchall()
		db.close()

		#TODO random
	except Exception, e:
		return -1

def set_my_dairy(dairy):
	try:
		print 'ddskjs fucking!!'
		print dairy
		print '#@#@$dfglkjdflgdjlkg'
		print dairy['user_idx'],c_idx,current_time,dairy['content'],dairy['subject'],dairy['image']
	
		db = MySQLdb.connect("localhost","root",'y0108009','hackaton')
		cursor = db.cursor()
		c_idx = '15'
		cursor.execute("Insert into dairy value(%s,%s,'2012-11-11 11:11:11',\'%s\',%s)"% (dairy['user_idx'],c_idx,dairy['content'],dairy['subject']))
		db.commit()
		db.close()

		return 0
	except Exception, e:
		return -1

def set_reply(reply):
	try:
		db = MySQLdb.connect("localhost","root",'y0108009','hackaton')
		cursor = db.cursor()
		cursor.execute("Insert into reply value(%d,%s,%s)"% (reply['c_idx'],reply['content'],reply['is_frist']))
		db.commit()
		db.close()
		print 'bbbb'
		return 0
	except Exception, e:
		print 'aaaaaaa'
		return -1


class Dairy_Handler(tornado.websocket.WebSocketHandler):
	def open(self):
		print("Websocket opened")

	def on_message(self,msg):
		print 'on message'
		print msg
		result = ''
		self.write_message("ll")
		js = json.loads(msg)
		print js['type']
		#image_string = cStringIO.StringIO(base64.b64decode(msg['image']))
		#image = Image.open(image_string)
		#image.save('out.jpg')
		if js['type'] == 'showMyList':
			#json format => {'type':'showMyList','user_idx':int}
			result = get_dairy_list(js['user_idx'])
		elif js['type'] == 'showMyDairy':
			#json format => {'type':'showMyDairy','user_idx':int,'c_idx':int}
			result = get_my_dairy(js['c_idx'])
		elif js['type'] == 'showOtherDairy':
			#json format => {'type':'showOtherDairy','user_idx':int,'number':int}
			result = get_other_dairy(js['user_idx'],js['number'])
		elif js['type'] == 'showReply':
			#json format => {'type':'showReply','c_index':int}
			result = get_reply(js['c_idx'])
		elif js['type'] == 'writeMyDairy':
			print 'writemydairy'
			print js['dairy']['content']
			print js['dairy']
			#json format => {'type':'writeMyDairy','dairy':{'user_idx':int,'content:'@@','subject':int,'image':'null or imagestream'}}
			result = set_my_dairy(js['dairy'])
		elif js['type'] == 'writeReply':
			#json format => {'tyep':'writeReply','reply':{'content':'@@@',c_idx:int,is_frist:boolean}}
			result = set_reply(js['reply'])
				
		#self.write_message(result)

		#TODO
		#self.write_message(message)

	def on_close(self):
		print "bye"





		#{'content':{'content':'dd','subject':'22','oimag'}}



