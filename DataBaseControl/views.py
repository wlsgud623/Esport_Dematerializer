
from django.shortcuts import render, redirect
from django.contrib import messages, auth 
# Create your views here.

import firebase_admin
from firebase_admin import firestore as fs, credentials as cr, auth as au
from . import storebase
import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
import chardet
from django.http import JsonResponse
from google.cloud import firestore

try:
    nowapp = firebase_admin.get_app(name='datacontrol')
    firebase_admin.delete_app(nowapp)
except:
    pass
creddata = cr.Certificate('shoes-finder-project-firebase-adminsdk-o2rqq-a710ffd892.json')
appdata = firebase_admin.initialize_app(creddata,name='datacontrol')
store = fs.client(appdata)
print(appdata.name)




def DataControl(request):
    return render(request,"DataBase.html")
def Shose_Data_Load(request):

    Shose = store.collection(u'shose').order_by(u'name').stream()
    Shose_data =[]
    i = 0
    for Shose_load in Shose:
        """
        Shose_load.reference.delete({
            u'ID':fs.DELETE_FIELD,
            u'comment':fs.DELETE_FIELD,
        })
        """
        Shose_data.append(Shose_load.to_dict())
        #print(Shose_data)
    
    return render(request, "ShoseData.html", {'Shose':Shose_data})
    
def Shose_Data_View(request, Shosename):

    Shose = store.collection(u'shose').where(u'name',u'==',Shosename).stream()
    for Shose_data in Shose:
        Shose_data_load = storebase.Shose_Data_Store.from_dict(Shose_data.to_dict())
        if Shose_data_load:
            break
    print(Shosename)
    print(Shose_data_load)
    Shose_dic = Shose_data_load.to_dict()
    Shosepath = Shose_data.reference.path
    Shosepathlist = Shosepath.split('/')
    Shosecode = Shosepathlist[1]
    if request.COOKIES.get(u'Shosecode') == Shosecode:
        print(Shosecode)
        return render(request,"ShoseDataView.html",{"Shose":Shose_dic})
    else:
        print(Shosecode)
        print(request.COOKIES.get(u'Shosecode'))
        usertoken = au.verify_id_token(request.session[u'uid'],app=appdata)
        useruid = usertoken[u'uid']
        userstore = storebase.Get_User_Store(useruid)
        username = userstore[u'name']
        timezone = datetime.timezone(datetime.timedelta(hours=9))
        timestamp = datetime.datetime.now(timezone)
        #request.encoding = 'utf-8'
        #print(request.encoding)
        logs= storebase.User_logs(useruid,username,timestamp,Shose_dic[u'name'],"Read")
        logs.Log_Add_Store()
        logsdic = logs.to_dict()
#        def replace_space(dic):
#            for key, value in dic.items():
#                if isinstance(value,str):
#                    replacespace = value.replace(" ","-")
#                    dic[key] = replacespace
#            return dic
#        logsdic = replace_space(dic=logsdic)
        logsJson = json.dumps(logsdic,cls=DjangoJSONEncoder,ensure_ascii=False)
        
        #with open("/json/logsJson")
        response = render(request,"ShoseDataView.html",{"Shose":Shose_dic})
        response.set_cookie(u'Shosecode',Shosecode,6000)
        response['logs'] = logsJson
        return response
    
def Shose_Load_Data(request, Shosename):
    Shose = store.collection(u'shose').where(u'name',u'==',Shosename).stream()
    for Shose_data in Shose:
        Shose_data_load = storebase.Shose_Data_Store.from_dict(Shose_data.to_dict())
        if Shose_data_load:
            break
    Shose_dic = Shose_data_load.to_dict()
    Shose_dic_jsom = json.dumps(Shose_dic,cls=DjangoJSONEncoder,ensure_ascii=False)
    return render(request,"ShoseDataView.html",{"Shose":Shose_dic})

def Shose_add_New(request):
    if request.method == "POST":
        Shosecode = request.POST.get('code')
        Shosename = request.POST.get('name')
        Shosebrand = request.POST.get('brand')
        Shoseprice = int(request.POST.get('price'))
        Shosecolor = request.POST.get('color').split(' ')
        Shoseimage = request.POST.get('url')
        storebase.Shose_Data_Store.Shose_Add_Store(Shosecode, Shosename, Shosebrand, Shoseprice, Shosecolor, Shoseimage)
        return redirect('DataBase:Shose')
    else:
        return render(request,"AddShose.html")

def Shose_Back_Comment(request, Shosename):
    return redirect(Shose_Load_Data,name=Shosename,reqeust=request)
def Shose_Change_Data(request, Shosename):
    Shose = store.collection(u'shose').where(u'name',u'==',Shosename).stream()
    for Shose_data in Shose:
        Shose_data_load = storebase.Shose_Data_Store.from_dict(Shose_data.to_dict())
        if Shose_data_load:
            break
    Shose_dic = Shose_data_load.to_dict()
    print(Shose_dic)
    return render(request, "ShoseDataChange.html",{"Shose":Shose_dic})
def Shose_Data_Change(request):
    Shosename = request.POST.get('name')
    Shosebrand = request.POST.get('brand')
    Shoseprice = int(request.POST.get('price'))
    Shosecolor = request.POST.get('color').split(' ')
    Shoseimage = request.POST.get('url')
    storebase.Shose_Data_Store.Shose_Store_Update(Shosename, Shosebrand, Shoseprice, Shosecolor, Shoseimage)
    return redirect(Shose_Load_Data,Shosename=Shosename,request=request)

def Shose_del(request, Shosename):
    if request.method == "POST":
        storebase.Shose_Data_Store.Shose_Del_Store(Shosename)
        return redirect("DataBase:Shose")
    else:
        return render(request, "ShoseDel.html",{"name":Shosename})

def Shose_Comment_List(request, Shosename):
    timezone = datetime.timezone(datetime.timedelta(hours=9))
    print(Shosename)
    Shoseref = store.collection(u'comment').where(u'shose',u'==',Shosename)
    Shosestore = Shoseref.order_by(u'timestamp',direction=firestore.Query.DESCENDING).get()
    
    Commentlist = []
    i = 0
    print(Shosestore)
    print(type(Shosestore))
    try:
        for Comment in Shosestore:
            if Comment.exists :
                paths = Comment.reference.path
                ref = paths.split('/')
                Commentpath = ref[1]
                Commentdic = Comment.to_dict()
                Commentdic[u'path'] = Commentpath
                Commentdic[u'number'] = i
                i += 1
                Commentlist.append(Commentdic)
            else:
                print("error")
                break
            Commentjson = json.dumps(Commentlist,DjangoJSONEncoder,ensure_ascii=False)
        return render(request, "ShoseCommentList.html",{"Commentlist":Commentlist, "Shosename":Shosename})
    except:
        print("error")
        return render(request, "ShoseCommentList.html",{"Commentlist":Commentlist, "Shosename":Shosename})

def Shose_Comment_Views(request, Shosename, path):
    cref = store.collection(u'comment').document(path).get()
    Comment = storebase.Shose_Comment.from_dict(cref.to_dict())
    return render(request, "ShoseCommentView.html",{"comment":Comment,"name":Shosename,"path":path})

def Shose_Comment_goto_Add(request,Shose):
    usertoken =au.verify_id_token(request.session[u'uid'],app=appdata)
    useruid = usertoken[u'uid']
    userstore = storebase.Get_User_Store(useruid)
    username = userstore[u'name']
    return render(request, "ShoseCommentAdd.html",{"username":username,"Shosename":Shose})

def Shose_Comment_Add(request,Shosename):
    print(request.method)
    if request.method == 'POST':
        timezone = datetime.timezone(datetime.timedelta(hours=9))
        CommentName=request.POST.get('name')
        CommentTimestamp = datetime.datetime.now(timezone)
        Commentcomment = request.POST.get('comment')
        CommentUid=request.POST.get('uid')
        CommentShose = Shosename
        Comment = storebase.Shose_Comment(CommentShose,CommentTimestamp,CommentName,CommentUid,Commentcomment)
        Comment.Add_Comment()
        return redirect("DataBase:CommentList",Shosename)
    else:
        usertoken =au.verify_id_token(request.session[u'uid'],app=appdata)
        useruid = usertoken[u'uid']
        userstore = storebase.Get_User_Store(useruid)
        username = userstore[u'name']
        print(username)
        return render(request, "ShoseCommentAdd.html",{"username":username,"Shosename":Shosename,"uid":useruid})
def Shose_Comment_goto_Rewrite(request,Shosename,timestamp):
    sref = store.collection(u'shose').where(u'shose',u'==',Shosename).stream()
    for ssref in sref:
        if ssref:
            break
    ref = ssref.reference.path
    rref = ref.split("/")
    code = rref[1]
    cref = store.collection(u'shose').document(code).collection(u'Comment').document(timestamp).get()
    Comment = storebase.Shose_Comment.from_dict(cref.to_dict())
    return render(request,"ShoseCommentChange.html",{"Comment":Comment,"Shosename":Shosename,"timestamp":timestamp})

def Shose_Comment_Rewrite(request,Shosename,path):
    if request.method == 'POST':
        cref = store.collection(u'comment').document(path).get()
        Commentref = cref.to_dict()
        timezone = datetime.timezone(datetime.timedelta(hours=9))
        CommentName = request.POST.get('name')
        print(Commentref.get(u'timestamp'))
        print(datetime.datetime.now())
        print(datetime.datetime.now(timezone))
        CommentTimestamp = Commentref.get(u'timestamp').astimezone(timezone)
        Commentcomment = request.POST.get('comment')
        CommentRewrite_Timestamp = datetime.datetime.now(timezone)
        CommentUid = request.POST.get('uid')
        storebase.Shose_Comment.Update_Comment(CommentUid,Shosename,CommentTimestamp,CommentName,Commentcomment,CommentRewrite_Timestamp)
        return redirect("DataBase:ShoseCommentView",Shosename,path)
    else:
        cref = store.collection(u'comment').document(path).get()
        Comment = storebase.Shose_Comment.from_dict(cref.to_dict())
        usertoken =au.verify_id_token(request.session[u'uid'],app=appdata)
        useruid = usertoken[u'uid']
        if useruid == Comment.uid:
            return render(request,"ShoseCommentChange.html",{"Comment":Comment,"Shosename":Shosename,"path":path,"uid":useruid})
        else:
            messages.error(request,"작성자만 수정을 할 수 있습니다.")
            return redirect("DataBase:ShoseCommentView",Shosename,path)


def Shose_Comment_goto_Del(request,Shosename,timestamp):
    usertoken =au.verify_id_token(request.session[u'uid'],app=appdata)
    useruid = usertoken[u'uid']
    userstore = storebase.Get_User_Store(useruid)
    uid = userstore[u'uid']
    sref = store.collection(u'shose').where(u'shose',u'==',Shosename).stream()
    for ssref in sref:
        if ssref:
            break
    cref = ssref.collection(u'Comment').document(timestamp)
    Comment = storebase.Shose_Comment.from_dict(cref.to_dict())
    if uid == Comment.uid or userstore.get(u"admin"):
    
        return render(request, "ShoseCommentDel.html",{"name":Shosename,"timestamp":timestamp})
    else:
        messages.error(request,"작성자와 운영자만 삭제를 할 수 있습니다.")
        return redirect("DataBase:ShoseCommentView",Shosename,timestamp)
    
def Shose_Comment_Del(request,Shosename,path):
    if request.method == "POST":
        usertoken =au.verify_id_token(request.session[u'uid'],app=appdata)
        useruid = usertoken[u'uid']
        userstore = storebase.Get_User_Store(useruid)
        uid = userstore[u'uid']
        cref = store.collection(u'shose').document(path).get()
        Comment = storebase.Shose_Comment.from_dict(cref.to_dict())
        if uid == Comment.uid or usertoken.get(u"admin"):
            storebase.Shose_Comment.Del_Comment(Comment.timestamp,Shosename,uid)
            return redirect("DataBase:CommentList",Shosename)
        else:
            messages.error(request,"작성자와 운영자만 삭제를 할 수 있습니다.")
            return redirect("DataBase:ShoseCommentView",Shosename,path)
    else:
        return render(request, "ShoseCommentDel.html",{"name":Shosename,"path":path})

def Logs_List(request):
    sref = store.collection(u'logs').order_by(u'timeStamp',direction=firestore.Query.DESCENDING).stream()
    LogsList = []
    timezone = datetime.timezone(datetime.timedelta(hours=9))
    for logsl in sref:
        fullpath = logsl.reference.path
        fullpath = fullpath.split("/")
        path = fullpath[1]
        logs = logsl.to_dict()
        timepath = logs[u'timeStamp']
        timepath = timepath.astimezone(timezone)
        logs[u'path'] = path
        LogsList.append(logs)
    return render(request, "LogsList.html",{u'Logs':LogsList})

def Logs_View(request,path):
    logs_ref = store.collection(u'logs').document(path)
    logs_dic = logs_ref.get().to_dict()
    return render(request, "LogsView.html",{"Logs":logs_dic,"path":path})

def Logs_Del(request,path):
    usertoken = au.verify_id_token(request.session[u'uid'],app=appdata)
    if request.method == "POST":
        if usertoken.get(u'admin') == True:
            storebase.User_logs.Log_Del_Store(path)
            return redirect("DataBase:Logs")
        else:
            messages.error(request,"운영자만 삭제를 할 수 있습니다.")
            return redirect("DataBase:LogsView",path)
    else:
        return render(request,"LogsDel.html",{"path":path})

def User_List(request):
    sref = store.collection(u'user').order_by(u'uid').stream()
    UserList = []
    for User in sref:
        UserDic = User.to_dict()
        if UserDic.get(u'admin') is None:
            UserDic[u'admin'] = False
        UserList.append(UserDic)
    
    return render(request, "UserList.html", {"UserList":UserList})

def User_View(request, uid):
    User = storebase.Get_User_Store(uid)
    return render(request, "UserViews.html",{"User":User})

def User_Change(request, uid):
    if request.method == "POST":
        uid = request.POST.get(uid)
        email = request.POST.get('email')
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        admin = request.POST.get('admin[]')
        if not admin:
            admin = True
        else:
            admin = False
        au.update_user(uid,email=email,display_name=name)
        storebase.Update_User_Store(uid,name,email,age,gender,admin)
        au.set_custom_user_claims(uid, {u'admin': admin })
        return redirect("DataBAse:UsersView",uid)
    else:
        uref = storebase.Get_User_Store(uid)
        token = au.verify_id_token(request.session[u'uid'],app=appdata)

        return render(request, "UserChange.html",{"User":uref,"admin":token[u'admin']})
def User_Del(request,uid):
    token = au.verify_id_token(request.session[u'uid'] ,app=appdata)
    if request.method == "POST":
        if token.get(u'admin')== True :
            storebase.Del_User_Store(uid)
            return redirect("DataBase:Users")
        elif token.get(u'uid') == uid:
            storebase.Del_User_Store(uid)
            au.delete_user(uid,app=appdata)
            auth.logout(request)
            return redirect("Home")
        else:
            messages.error(request,"운영자와 본인만 삭제를 할 수 있습니다.")
            return redirect("DataBase:UsersView",uid)
    else:
        return render(request, "UserDelete.html",{"uid":uid})
def User_Logs(request,uid):
    sref = store.collection(u'logs').where(u'uid',u'==',uid).order_by(u"timeStamp",direction=firestore.Query.DESCENDING).stream()
    LogsList = []
    if sref == None:
        return render(request, "UserLogsList.html",{u'Logs':LogsList})
    for logsl in sref:
        fullpath = logsl.reference.path
        fullpath = fullpath.split("/")
        path = fullpath[1]
        logs = logsl.to_dict()
        logs[u'path'] = path
        LogsList.append(logs)
    return render(request, "UserLogsList.html",{u'Logs':LogsList})
def User_Logs_View(request,uid,path):
    Logs = storebase.User_logs.Log_Get_Store(path)
    LogsList= Logs.to_dict()
    logsJson = json.dumps(Logs.to_dict(),cls=DjangoJSONEncoder,ensure_ascii=False)
    return render(request,"UserLogsView.html",{u'Logs':LogsList,u'uid':uid,u'path':path})
def User_Logs_Del(request,uid,path):
    usertoken = au.verify_id_token(request.session[u'uid'],app=appdata)
    if request.method == "POST":
        if usertoken.get(u'admin') == True:
            storebase.User_logs.Log_Del_Store(path)
            return redirect("DataBase:UsersLog",uid)
        else:
            messages.error(request,"운영자만 삭제를 할 수 있습니다.")
            return redirect("DataBase:UsersLogView",uid,path)
    else:
        return render(request,"UsersLogsDel.html",{"uid":uid,"path":path})
def User_Log_Json(request):
    print(request.method)
    if request.method == "POST":
        print(request.META['CONTENT_TYPE'])
        if request.META['CONTENT_TYPE'] == 'application/json':
            print(request.body)
            request_json = json.loads(request.body.decode('utf-8'))
            Shose = store.collection(u'shose').where(u'name',u'==',request_json[u'shose']).stream()
            for Shose_data in Shose:
                Shose_data_load = storebase.Shose_Data_Store.from_dict(Shose_data.to_dict())
                if Shose_data_load:
                    break
            Shose_dic = Shose_data_load.to_dict()
            username = request_json[u'name']
            useruid = request_json[u'uid']
            timezone = datetime.timezone(datetime.timedelta(hours=9))
            timestamp = datetime.datetime.now(timezone)
            logs= storebase.User_logs(useruid,username,timestamp,Shose_dic[u'name'],"Read")
            logs.Log_Add_Store()
            logsdic = logs.to_dict()
            return JsonResponse(logsdic)
        else:
            Jsons = {
                u'error':'error',
            }
            return JsonResponse(Jsons)
    else:
        Jsons = {
            u'error':'error',
        }
        return JsonResponse(Jsons)
    




