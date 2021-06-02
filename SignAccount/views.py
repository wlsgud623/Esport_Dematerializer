from django import utils
from django.shortcuts import render, redirect
import firebase_admin
from firebase_admin import auth, firestore, credentials
import os,sys
import pyrebase
from django.contrib import auth as au
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from DataBaseControl import storebase as data
from django.utils import timezone
from datetime import datetime
import time
#from..DataBaseControl import views

# Create your views here.
 
firebaseConfig = {
    "apiKey": "AIzaSyBbj2fEGcpTvKkr1j4Rtft5D_VNMx3ljSo",
    "authDomain": "shoes-finder-project.firebaseapp.com",
    "databaseURL": "https://shoes-finder-project-default-rtdb.firebaseio.com",
    "projectId": "shoes-finder-project",
    "storageBucket": "shoes-finder-project.appspot.com",
    "messagingSenderId": "548574407922",
    "appId": "1:548574407922:web:15243e1df328ace328f46b",
    "measurementId": "G-VP2CMGGNFN"
}

firebase = pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()
try:
    nowapp = firebase_admin.get_app(name='sign')
    firebase_admin.delete_app(nowapp)
except:
    pass
credsign = credentials.Certificate('shoes-finder-project-firebase-adminsdk-o2rqq-536745041e.json')
appsign = firebase_admin.initialize_app(credsign,name='sign')
store = firestore.client(appsign)
print(appsign.name)
print(timezone.now())
nowtime = datetime.now()
print(nowtime.timestamp())
#print(app.name())

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = authe.sign_in_with_email_and_password(email,password)
            """
            try:
                print(user['localId'])
                print(type(user['localId']))
                user_id = auth.get_user(user['localId'])
            except Exception as e:
                print("에러가 발생했습니다.", e)
                message = "등록되지 않은 회원입니다."
                #print(user_id.error)
                return render(request,"SignIn.html",{"message":message})
            """
        except:
            message = "잘못된 이메일 주소거나 비밀번호입니다."
            return render(request,"SignIn.html",{"message":message})
    #print(user_id)
        session_id = user['idToken']
        print(user)
        print(session_id)
        request.session['uid'] = str(session_id)
        request.session['email'] = str(email)
        token = auth.verify_id_token(request.session[u'uid'],app=appsign)
        if token.get(u'admin') != True:
            auth.set_custom_user_claims(token[u'uid'],{u'admin':False})
        uid = token[u'uid']
        print(token.get(u'admin'))
        print(token)
        users = auth.get_user(uid)

    #if uid == "7Q7Mcmqpy5Vizg0M5FRArj5GPwo2":
    #    auth.set_custom_user_claims(uid,{'admin':True})

        return render (request,"Welcome.html",{"e":email})
    else:
        return render(request,"SignIn.html")
def logout(request):
    au.logout(request)
    return redirect("Home")
def SignUp(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = int(request.POST.get('age'))
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        #timestamp = time.mktime(time.strptime("%B %d, %Y - %H:%M:%S",timezone.now()))

        #print(app.name())
        user = auth.create_user(email=email,password=password,display_name=name,app=appsign)
        print(user.uid)
        try:
            user_correct = auth.get_user_by_email(email,app=appsign)
        except:
            message = "회원 등록에 실패했습니다."

            return render(request, "SignUp.html",{"message":message})
        print(user_correct.uid)

        data.Add_User_Store(user.uid,name,age,email,gender)
        auth.set_custom_user_claims(user.uid, {u'admin':False})
        #UserAdd
        return redirect("SAccount:signin")
    else:
        return render(request, "SignUp.html")

def deleteuser(request):
    token = auth.verify_id_token(request.session[u'uid'],app=appsign)
    if request.method == 'POST':
        token = auth.verify_id_token(request.session[u'uid'],app=appsign)
        print(token)
        user_id = token[u'uid']
        print(user_id)
        data.Del_User_Store(user_id)
        auth.delete_user(user_id,app=appsign)
        au.logout(request)
        return redirect("Home")
    else:
        return render(request,"DeleteUser.html")
def deleteCancel(request):
    token = auth.verify_id_token(request.session[u'uid'],app=appsign)
    email = token[u'email']
    return render(request,"Welcome.html",{'e':email})
def GetUsers(request):
    token = auth.verify_id_token(request.session[u'uid'],app=appsign)
    user_info = data.Get_User_Store(token[u'uid'])
    name = user_info[u'name']
    email = user_info[u'email']
    age = user_info[u'age']
    gender = user_info[u'gender']
    
    return render(request, "", {"name":name, "email":email, "age":age, "gender":gender})
def UpdateUsers(request):
    token = auth.verify_id_token(request.session[u'uid'],app=appsign)
    uid = token[u'uid']
    email = request.POST.get('email')
    name = request.POST.get('name')
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    admin = request.POST.get('admin')
    auth.update_user(uid,email=email,display_name=name)
    data.Update_User_Store(uid,name,email,age,gender,admin)
    auth.set_custom_user_claims(uid, {u'admin': admin })
    return redirect("Home")
