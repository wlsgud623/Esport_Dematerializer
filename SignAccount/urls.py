from django.urls import path
from django.urls import re_path
import sys

from . import views

app_name = "SAccount"

urlpatterns = [
    path('login/',views.signin,name="signin"),
    path('logout/',views.logout,name="logout"),
    path('SignUp/',views.SignUp,name="SignUp"),    
    path('deleted/',views.deleteuser,name="del"),
    path('cancel/',views.deleteCancel,name="cancel"),
]