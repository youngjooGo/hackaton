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
import uuid
import datetime
import random


def get_dairy_list(index):
	try:
		db = MySQLdb.connect("localhost",'root','y0108009','hackaton')
		cursor = db.cursor()
		cursor.execute("select c_idx from diary where user_idx = %d" % index)
		data = cursor.fetchall()
		db.close()
		result_list = []
		for i in data:
			result_list.append(i[0])
		result = "{'tag':'c_idx_list','list':"+str(result_list)+"}"
		return result
	except Exception, e:
		return 'fail'

def get_my_dairy(index):
	try:
		db = MySQLdb.connect("localhost","root",'y0108009','hackaton')
		cursor = db.cursor()
		#cursor.execute("select * from diary where c_idx = %d" % index)
		cursor.execute("select * from diary")
		data = cursor.fetchall()
		db.close()
		lenght = len(data)
		idx = random.randrange(0,lenght)
		result_like = get_like(data[idx][1])
		result = "{'tag':'dairy','content':{'c_idx':"+str(data[idx][1])+",'date':\'"+str(data[idx][2])+"\','content':\'"+str(data[idx][3])+"\','subject':"+str(data[idx][4])+",'like':"+str(result_like)+"}}"
		return result
	except Exception, e:
		import traceback
		traceback.print_exc()
		return 'fail'

def get_like(index):
	try:
		db = MySQLdb.connect("localhost","root",'y0108009','hackaton')
		cursor = db.cursor()
		cursor.execute("select * from amountLike where c_idx = %d" % index)
		data = cursor.fetchone()
		db.close()
		result = 0;
		for i in data:
			result += i[1]
		return str(result)
	except Exception, e:
		import traceback
		traceback.print_exc()
		return 'fail'

def get_other_dairy(index):
	try:
		db = MySQLdb.connect("localhost","root",'y0108009','hackaton')
		cursor = db.cursor()
		cursor.execute("select * from diary where user_idx is not %d" % index)
		data = cursor.fetchall()
		db.close()
		lenght = len(data)
		idx = random.randrange(0,lenght)
		result = "{'c_idx':"+str(data[idx][1])+",'date':"+str(data[idx][2])+",'content':"+str(data[idx][3])+",'subject':"+str(data[idx][4])+"}"
		return data[idx]
	except Exception, e:
		return 'fail'

def set_my_dairy(dairy):
	try:
		
		print 'asdfs'
		db = MySQLdb.connect("localhost","root",'y0108009','hackaton')
		cursor = db.cursor()
		c_idx = uuid.uuid4().int & (1<<16)-1
		c = datetime.datetime.now()
		date = c.isoformat()
		cursor.execute("Insert into diary(user_idx,c_idx,date,content,subject) value(%d,%s,\'%s\',\'%s\',%d)"% (dairy['user_idx'],c_idx,date,dairy['content'].encode('utf-8'),dairy['subject']))
		db.commit()
		db.close()

		return 'success'
	except Exception, e:
		import traceback
		traceback.print_exc()
		return 'fail'

def set_like(reply):
	try:
		db = MySQLdb.connect("localhost","root",'y0108009','hackaton')
		cursor = db.cursor()
		cursor.execute("Insert into amountLike value(%d,%d)"% (reply['c_idx'],reply['is_like']))
		db.commit()
		db.close()
	
		return 'success'
	except Exception, e:
		import traceback
		traceback.print_exc()
		return 'fail'


class Dairy_Handler(tornado.websocket.WebSocketHandler):
	def open(self):
		print("Websocket opened")

	def on_message(self,msg):
		try:
			print 'on message'
			print msg
			msg = msg.replace("\n", "\\n")
			result = ''

			js = json.loads(msg)
			
			if js['type'] == 'showMyList':
				#json format => {'type':'showMyList','user_idx':int}
				result = get_dairy_list(js['user_idx'])
			elif js['type'] == 'showMyDairy':
				print 'showMyDairy'
				#json format => {'type':'showMyDairy','user_idx':int,'c_idx':int}
				result = get_my_dairy(js['c_idx'])
			elif js['type'] == 'showOtherDairy':
				#json format => {'type':'showOtherDairy','user_idx':int,'number':int}
				result = get_other_dairy(js['user_idx'])
			#elif js['type'] == 'showLike':
				#json format => {'type':'showLike','c_index':int}
			#	result = like_reply(js['c_idx'])
			elif js['type'] == 'writeMyDairy':
				print 'writemydairy'
				print js['dairy']['content']
				print js['dairy']
				#json format => {'type':'writeMyDairy','dairy':{'user_idx':int,'content:'@@','subject':int,'image':'null or imagestream'}}
				result = set_my_dairy(js['dairy'])
			elif js['type'] == 'writeLike':
				#json format => {'tyep':'writeLike','like':{'c_ids':'@@@',is_like':int}}
				result = set_like(js['like'])
			
			print result
			self.write_message(result)

			#TODO
			#self.write_message(message)
		except Exception, e:
			print '#@#@$@#$@#$@#$@#@'
			import traceback
			traceback.print_exc()

	def on_close(self):
		print "bye"





		#{'content':{'content':'dd','subject':'22','oimag'}}



