from functools import update_wrapper
from django.shortcuts import render
import firebase_admin
from firebase_admin import auth, firestore, credentials
credsign = credentials.Certificate('shoes-finder-project-firebase-adminsdk-o2rqq-536745041e.json')
appsign = firebase_admin.initialize_app(credsign)
def homePage(request):
    print(request.session.__dict__)
    print(request.session.__class__)
    if request.session.get('uid') :
        try:
            auth.verify_id_token(request.session[u'uid'],check_revoked=True)
        except:
            render(request,"Home.html")
        return render(request,"Welcome.html",{"e":request.session[u'email']})
    return render (request,"Home.html")
