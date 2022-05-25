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
