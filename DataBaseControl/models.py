from django.db import models
import firebase_admin
from firebase_admin import firestore as fs, credentials as cr

# Create your models here.
"""
cred = cr.Certificate("shoes-finder-project-firebase-adminsdk-o2rqq-39cbe27215.json")
app = firebase_admin.initialize_app(cred)
db = fs.client()

class User_list(models.Model):
    uid = models.CharField(primary_key=True,default=)
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(max_length=100)
    email = models.EmailField(max_length=200)
    password = models.TextField()
"""
