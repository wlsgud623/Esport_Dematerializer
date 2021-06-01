import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
import pyrebase

cred = credentials.Certificate('shoes-finder-project-firebase-adminsdk-o2rqq-b308bbaa36.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://shoes-finder-project-default-rtdb.firebaseio.com/'
})
db = firestore.client()