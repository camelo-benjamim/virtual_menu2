from django import urls
from django.db.models.fields import CharField 
from django.urls.conf import path, include
from accounts.views import *
from django.contrib import admin

urlpatterns = [
    path('', SignUp),
    path('user/', include('django.contrib.auth.urls')),
    path('edit/',ChangeUsr),
    path('user_delete/',usrDelete),
    path('user_deleted/',userDeleted),
    
]
