from cmath import atanh
from django.shortcuts import render
from django.urls import path
from menu_garcom.views import *
##
urlpatterns = [
    ## VIEWS DO USUÁRIO
    ##RESTAURANTE
    path('conectar/<int:codigo>/',adicionarConexao),
    path('',fazerPedido),
    path('escolher_mesa',escolherMesa),
    path('escolher_mesa/<str:mesa>',argumentoMesa),
    path('confirmar_pagamento/',confirmarPagamento),
    
]                  