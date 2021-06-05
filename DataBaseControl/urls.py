from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.urls import include
from . import views

app_name = "DataBase"

urlpatterns = [
   path('DataStore/',views.DataControl,name="data"),
   path('ShoseData/',views.Shose_Data_Load,name="Shose"),
   path('ShoseView/<str:Shosename>',views.Shose_Data_View,name="ShoseData"),
   path('ShoseAdd/',views.Shose_add_New,name="ShoseAdd"),
   path('ShoseChange/<str:Shosename>',views.Shose_Change_Data,name="ShoseChange"),
   path('ShoseChange/<str:Shosename>/Done',views.Shose_Data_Change,name="ShoseDataChange"),
   path('ShoseDel/<str:Shosename>',views.Shose_del,name="ShoseDelete"),
   path('ShoseComment/<str:Shosename>',views.Shose_Comment_List,name="CommentList"),
   path('ShoseComment/<str:Shosename>/Add',views.Shose_Comment_Add,name="AddComment"),
   path('ShoseComment/<str:Shosename>/<str:path>',views.Shose_Comment_Views,name="ShoseCommentView"),
   path('ShoseComment/<str:Shosename>/<str:path>/Change',views.Shose_Comment_Rewrite,name="ChangeComment"),
   path('ShoseComment/<str:Shosename>/<str:path>/Delete',views.Shose_Comment_Del,name="CommentDelete"),
   path('Logs/', views.Logs_List,name="Logs"),
   path('Logs/<str:path>/Del',views.Logs_Del,name="LogsDelete"),
   path('Logs/<str:path>',views.Logs_View,name="LogsView"),
   path('Users/',views.User_List,name="Users"),
   path('Users/<str:uid>',views.User_View,name="UsersView"),
   path('Users/<str:uid>/Change',views.User_Change,name="UsersChange"),
   path('Users/<str:uid>/Delete',views.User_Del,name="UsersDelete"),
   path('Users/<str:uid>/logs',views.User_Logs,name="UsersLog"),
   path('Users/<str:uid>/<str:path>',views.User_Logs_View,name="UsersLogView"),
   path('Users/<str:uid>/<str:path>/Delete',views.User_Logs_Del,name="UsersLogDel"),
   path('apijson/',views.User_Log_Json,name="UserLogsJson"),
   


   


]
