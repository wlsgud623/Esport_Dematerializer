import firebase_admin
from firebase_admin import firestore as fs, credentials as cr
import scrypt
import base64
from Crypto.Protocol.KDF import scrypt
import datetime
from django.contrib import messages
# Create your models here.

"""
class User_list(models.Model):
    uid = models.CharField(primary_key=True,default=)
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(max_length=100)
    email = models.EmailField(max_length=200)
    password = models.TextField()
"""
try:
    nowapp = firebase_admin.get_app(name='data')
    firebase_admin.delete_app(nowapp)
except:
    pass
creddata = cr.Certificate('shoes-finder-project-firebase-adminsdk-o2rqq-a710ffd892.json')
appdata = firebase_admin.initialize_app(creddata,name='data')
store = fs.client(appdata)
print(appdata.name)

timezone = datetime.timezone(datetime.timedelta(hours=9))

class User_logs(object):
    def __init__(self, uid, user, timeStamp, shoses, category):
        self.user = user
        self.timeStamp = timeStamp
        self.shoses = shoses
        self.category = category
        self.uid = uid
    @staticmethod
    def from_dict(source):
        userlogs = User_logs(source[u'uid'],source[u'user'],source[u'timeStamp'],source[u'shoses'],source[u'category'])
        return userlogs
    def to_dict(self):
        dets = {
            u'uid':self.uid,
            u'user':self.user,
            u'timeStamp':self.timeStamp,
            u'shoses':self.shoses,
            u'category':self.category,

        }
        return dets
    def __repr__(self):
        return(
            f'User_logs( \
                uid={self.uid}, \
                user={self.user}, \
                timeStamp={self.timeStamp}, \
                shoses={self.shoses}, \
                category={self.category},\
            )'
        )
    def Log_Add_Store(self):
        doc = self.to_dict()
        ref = store.collection(u'logs').document()
        ref.set(
            {
                u'ServerTimeStamp':fs.SERVER_TIMESTAMP,
            }
        )
        ref.set(doc,merge=True)
        
    def Log_Get_Store(path):
        ref = store.collection(u'logs').document(path)
        Log = User_logs.from_dict(ref.get().to_dict())
        return Log
    def Log_Del_Store_auto(uid):
        log_ref = store.collection(u'logs')
        query = log_ref.where(u'uid',u'==',uid).order_by(u'timeStamp').limit_to_last(1000)
        doc = query.stream()
        i = 0
        for doce in doc:
            if i == 999:
                log_last = User_logs.from_dict(doce.to_dict())
            i += 1
        query_last = log_ref.where(u'uid',u'==',uid).where(u'timeStamp',u'<',log_last.timeStamp).stream()
        for doce in query_last:
            doce.delete()
    def Log_Del_Store(path):
        log_ref = store.collection(u'logs')
        log_ref.document(path).delete()

class Shose_Comment(object):
    def __init__(self, timestamp, name, uid, comment):
        self.timestamp = timestamp
        self.name = name
        self.uid = uid
        self.comment = comment
        self.rewrite = False
        self.rewrite_timestamp = timestamp
    @staticmethod
    def from_dict(source):
        Comment = Shose_Comment(source[u'timestamp'],source[u'name'],source[u'uid'],source[u'comment'])
        Comment.rewrite = source[u'rewrite']
        if Comment.rewrite == True:
            Comment.rewrite_timestamp = source[u'rewrite_timestamp']
        return Comment
    def to_dict(self):
        dic = {
            u'timestamp':self.timestamp,
            u'name':self.name,
            u'uid':self.uid,
            u'comment':self.comment,
            u'rewrite':self.rewrite,
            u'rewrite_timestamp':self.rewrite_timestamp,
        }
        return dic
    def __repr__(self):
        return(
            f'User( \
                timestamp={self.timestamp}, \
                name={self.name}, \
                uid={self.uid}, \
                comment={self.comment}, \
                rewrite={self.rewrite}, \
                rewrite_timestamp={self.rewrite_timestamp}, \
            )'
        )
    def Add_Comment(self,shose):
        storeref = store.collection(u'shose').where(u'name',u'==',shose).stream()
        for storeshose in storeref:
            Comment = storeshose
            if Comment:
                break
        ref = Comment.reference.path
        rref = ref.split("/")
        shosecode = rref[1]
        storeref = store.collection(u'shose').document(shosecode).collection(u'Comment')
        storeref.document(datetime.datetime.strftime(self.timestamp,"%Y-%m-%d-%H-%M-%f")).set(self.to_dict())
        
    def Del_Comment(timestamp,shose,uid):
        storeref = store.collection(u'shose').where(u'name',u'==',shose).stream()
        for storeshose in storeref:
            Comment = storeshose
            if Comment:
                break
        ref = Comment.reference.path
        rref = ref.split("/")
        shosecode = rref[1]
        storeref = store.collection(u'shose').document(shosecode).collection(u'Comment').document(timestamp)
        stores = storeref.get().to_dict()
        if stores[u'uid'] == uid:
            storeref.delete()

    def Get_Comment(timestamp, shose):
        storeref = store.collection(u'shose').where(u'name',u'==',shose).stream()
        for storeshose in storeref:
            Comment = storeshose
            if Comment:
                break
        ref = Comment.reference.path
        rref = ref.split("/")
        shosecode = rref[1]
        storeref = store.collection(u'shose').document(shosecode).collection(u'Comment').document(timestamp)
        Commentref = storeref.get()
        CommentGet = Shose_Comment.from_dict(Commentref.to_dict)
        return CommentGet
    def Update_Comment(self,shose):
        storeref = store.collection(u'shose').where(u'name',u'==',shose).stream()
        for storeshose in storeref:
            Comment = storeshose
            if Comment:
                break
        ref = Comment.reference.path
        rref = ref.split("/")
        shosecode = rref[1]
        storeref = store.collection(u'shose').document(shosecode).colletcion(u'Comment').document(datetime.datetime.strftime(self.timestamp,"%Y-%m-%d-%H-%M-%f"))
        storeref.update({
            u'comment':self.comment,
            u'rewrite':True,
            u'name':self.name,
            u'rewrite_timestamp':fs.SERVER_TIMESTAMP,
        })
    def Update_Comment(shose,timestamp,name,comment,rewrite_timestmap):
        storeref = store.collection(u'shose').where(u'name',u'==',shose).stream()
        for storeshose in storeref:
            Comment = storeshose
            if Comment:
                break
        ref = Comment.reference.path
        rref = ref.split("/")
        shosecode = rref[1]
        storeref = store.collection(u'shose').document(shosecode).colletcion(u'Comment').document(datetime.datetime.strftime(timestamp,"%Y-%m-%d-%H-%M-%f"))
        storeref.update({
            u'comment':comment,
            u'rewrite':True,
            u'name':name,
            u'rewrite_timestamp':rewrite_timestmap,
        })

        

class User_list_store(object):
    def __init__(self, uid, name=None, email=None, age=None, gender=None):
        self.uid=uid
        if name:
            self.name=name
        if email:
            self.email=email
        if age:
            self.age=age
        if gender:
            self.gender=gender
        self.admin = False
        #self.favroite=favroite
        #self.logs=logs
    @staticmethod
    def from_dict(source):
        User = User_list_store(source[u'uid'])
        if u'name' in source:
            User.name = source[u'name']
        if u'email' in source:
            User.email = source[u'email']
        if u'age' in source:
            User.age = source[u'age']
        if u'gender' in source:
            User.gender = source[u'gender']
        if u'admin' in source:
            User.admin = source[u'admin']
        """
        if u'favroite' in source:
            User.favroite=source[u'favroite']
        if u'logs' in source:
            User.logs = source[u'logs']
        """
        return User
    def to_dict(self):
        dets = {
            u'uid':self.uid,
        }
        if self.name:
            dets[u'name'] = self.name
        if self.email:
            dets[u'email'] = self.email
        if self.age:
            dets[u'age'] = self.age
        if self.gender:
            dets[u'gender'] = self.gender
        dets[u'admin'] = self.admin
        """
        if self.favroite:
            dets[u'favroite'] = self.favroite
        if self.logs:
            dets[u'logs'] = self.logs
        """
        return dets
    def __repr__(self):
        return(
            f'User( \
                uid={self.uid}, \
                name={self.name}, \
                email={self.email}, \
                age={self.age}, \
                gender={self.gender}, \
                admins={self.admin}, \
            )'
        )
def Add_User_Store(uid,name=None,age=None,email=None,gender=None,admin=None):
    det = {u'uid':uid}
    if name:
        det[u'name'] = name
    if age:
        det[u'age'] = age
    if email:
        det[u'email'] = email
    if gender:
        det[u'gender'] = gender
    det[u'admin'] = False
    if admin:
        det[u'admin'] = True
    user = User_list_store.from_dict(det)
    store.collection(u'user').document(uid).set(user.to_dict())
def Del_User_Store(uid):
    def Del_User_Limit(ref,size):
        docm = ref.limit(size).stream()
        deleted = 0
        for doc in docm:
            print(f'Deleting doc {doc.id} => {doc.to_dict()}')
            doc.reference.delete()
            deleted = deleted + 1
        if deleted >= size:
            return Del_User_Limit(ref,size)
    store.collection(u'user').document(uid).delete()
def Get_User_Store(uid):
    user_ref = store.collection(u'user').document(uid)
    user_info = user_ref.get()
    print(user_info.to_dict())
    if user_info.exists:
        user = User_list_store.from_dict(user_info.to_dict())
        return user.to_dict()
    else:
        return None
def Update_User_Store(uid,name,email,age,gender,admin):
    user_ref = store.collection(u'user').document(uid)
    det = {}
    if name:
        det[u'name'] = name
    if email:
        det[u'email'] = email
    if age:
        det[u'age'] = age
    if gender:
        det[u'gender'] = gender
    if admin:
        det[u'admin'] = admin
    user_ref.update(det)
    
    
class Shose_Data_Store(object):

    def __init__(self, name, brand=None,  price=None, color=None, image=None):
        self.name = name
        if brand:
            self.brand = brand
        if price:
            self.price = price
        if color:
            self.color = color
        if image:
            self.image = image
        self.rate = 0
        self.user_count = 0
        self.user_total = 0.0
        self.comment_count = 0
    @staticmethod
    def from_dict(source):
        Shose = Shose_Data_Store(source[u'name'])
        if u'brand' in source:
            Shose.brand = source[u'brand']
        if u'price' in source:
            Shose.price = source[u'price']
        if u'color' in source:
            Shose.color = source[u'color']
        if u'image' in source:
            Shose.image = source[u'image']
        if u'rate' in source:
            Shose.rate = source[u'rate']
        if u'user_count' in source:
            Shose.user_count = source[u'user_count']
        if u'user_total' in source:
            Shose.user_total = source[u'user_total']
        if u'comment_count' in source:
            Shose.comment_count = source[u'comment_count']
        return Shose
    def to_dict(self):
        sdet = {
            u'name':self.name,
        }
        if self.brand:
            sdet[u'brand'] = self.brand
        if self.price:
            sdet[u'price'] = self.price
        if self.color:
            sdet[u'color'] = self.color
        if self.image:
            sdet[u'image'] = self.image
        if self.rate:
            sdet[u'rate'] = self.rate
        if self.user_count:
            sdet[u'user_count'] = self.user_count
        if self.user_total:
            sdet[u'user_total'] = self.user_total
        if self.comment_count:
            sdet[u'comment_count'] = self.comment_count
        return sdet
    def __repr__(self):
        return (
            f'Shose( \
                name={self.name}, \
                brand={self.brand}, \
                price={self.price}, \
                color={self.color}, \
                rate={self.rate}, \
                image={self.image}, \
            )'
        )
    
    def rate_cal(self,rate):
        self.user_count += 1
        self.user_total += rate
        self.rate = self.user_total/self.user_count
    def rate_update(self,rate,old_rate):
        self.user_total -= old_rate
        self.user_total += rate
        self.rate = self.user_total/self.user_count
        
    def Shose_Add_Store_Self(self, code):
        timestamp = datetime.datetime.now(timezone)
        store.collection(u'shose').document(code).set(self.to_dict)
        store.collection(u'shose').document(code).collection(u'Comment').document().set(
            {
                u'name':'',
                u'timestamp':timestamp,
                u'comment':'',
                u'rewrite':False,
            }
        )
    def Shose_Add_Store(code, name, brand=None, price=None, color=None, image=None):
        dic = {
            u'name':name
            }
        if brand:
            dic[u'brand'] = brand
        if price:
            dic[u'price'] = price
        if color:
            dic[u'color'] = color
        if image:
            dic[u'image'] = image
        timestamp = datetime.datetime.now(timezone)
        Shose = Shose_Data_Store.from_dict(dic)
        store.collection(u'shose').document(code).set(Shose.to_dict)
        store.collection(u'shose').document(code).collection(u'Comment').document().set(
            {
                u'name':'',
                u'timestamp':timestamp,
                u'comment':'',
                u'rewrite':False,
            }
        )
    
    def Shose_Get_Store(name):
        Shose_ref = store.collection(u'shose').where(u'name',u'==',name).stream()
        if Shose_ref:
            for Shose in Shose_ref:
                Shose_store = Shose_Data_Store.from_dict(Shose)
                if Shose_store:
                    break
        return Shose_store
    def Shose_Del_Store(name):
        def Shose_Del_Limit(ref,size):
            docm = ref.limit(size).stream()
            deleted = 0
            for doc in docm:
                print(f'Deleting doc {doc.id} => {doc.to_dict()}')
                doc.reference.delete()
                deleted = deleted + 1
            if deleted >= size:
                return Shose_Del_Limit(ref,size)
        Shose = store.collection(u'shose').where(u'name',u'==',name).stream()
        for Shose_one in Shose:
            Shose_Del_Limit(Shose_one.collection(u'comment'),10)
            Shose_one.delete()
    
    def Shose_Change_Name(self,name):
        self.name = name
    def Shose_Change_Brand(self,brand):
        self.brand = brand
    def Shose_Change_Price(self,price):
        self.price = price
    def Shose_Change_Color(self,color):
        self.color = color
    def Shose_Change_image(self,image):
        self.image =image
    def Shose_Store_Update(name=None, brand=None, price=None, color=None, image=None):
        Shose_ref = store.collection(u'shose').where(u'name',u'==',name).get()
        if not name==None:
            Shose_ref.update({u'name':name})
        if not brand==None:
            Shose_ref.update({u'brand':brand})
        if not price==None:
            Shose_ref.update({u'price':price})
        if not color==None:
            Shose_ref.update({u'color':color})
        if not image==None:
            Shose_ref.update({u'image':image})
        """Shose_ref.update(
            {
                u'rate': self.rate,
                u'user_count':self.user_count,
                u'user_total':self.user_total,
                u'comment_count':self.comment_count
            }
        )"""


    