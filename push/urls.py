from django.urls import path
from push.views import *

urlpatterns = [
    path('add_connection/', CreateConnection),
    path('test_message/<str:message>/',TestMessage),
    path('',explain),
]
