from datetime import datetime
import sys

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

from bot_alert import *

credentials = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(credentials)

db = firestore.client()

def userDB_reg(_message):
	try:
		doc_ref = db.collection('Users').document(f'{_message.from_user.id}')
		doc_ref.set({
			'uid'			:	_message.from_user.id,
			'num_of_uses'	:	1,
			'last_access'	:	f'{datetime.now()}'
		})
	except:
		error(f"[ ERROR ] in USERDB_REG of USER-{_message.from_user.id} : {sys.exc_info()[0]}.")

def userDB_update(_message):
	try:
		doc_ref = db.collection('Users').document(f'{_message.from_user.id}')
		num_of_uses = doc_ref.get().to_dict()['num_of_uses']
		doc_ref.update({
			'num_of_uses'	:	int(num_of_uses) + 1,
			'last_access'	:	f'{datetime.now()}'
		})
	except:
		error(f"[ ERROR ] in USERDB_UPDATE of USER-{_message.from_user.id} : {sys.exc_info()[0]}.")

def itemDB_add(_message, item_data):
	try:
		item_id, item_title, item_price = item_data.split(',')
		doc_ref = db.collection('Items').document(f'{item_id}')
		ret = 0
		if not doc_ref.get().exists:
			doc_ref.set({
				'iid'		:	item_id,
				'title'		:	item_title,
				'price'		:	item_price,
				'lookout'	:	[_message.from_user.id]
			})
		else:
			ex_lookout = doc_ref.get().to_dict()['lookout']
			if _message.from_user.id in ex_lookout:
				new_lookout = ex_lookout.remove(_message.from_user.id)
				doc_ref.update({
				'lookout'		:	new_lookout if new_lookout else []
				})
				ret = -1
			else:
				doc_ref.update({
					'lookout'		:	ex_lookout.append(_message.from_user.id)
				})
				ret = 1
			ex_price = doc_ref.get().to_dict()['price']
			if float(ex_price) > float(item_price):
				doc_ref.update({
					'price'		:	item_price
				})
				ret = [ret, doc_ref.get().to_dict(), item_data]
		return [ret]
	except:
		error(f"[ ERROR ] in ITEMDB_ADD of USER-{_message.from_user.id} : {sys.exc_info()[0]}.")
