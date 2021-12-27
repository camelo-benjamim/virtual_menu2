from django.shortcuts import render
from django.urls import path
from mesa.views import *

urlpatterns = [
    path('mesas/',verMesas),
    path('adicionar_mesa/',addMesa),
    path('deletar_mesa/<str:description>/', deleteMesa),
    path('mesaConsult/',mesaConsult),
]