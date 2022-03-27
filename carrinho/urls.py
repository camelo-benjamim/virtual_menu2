from django.shortcuts import render
from django.urls import path
from carrinho.views import *

urlpatterns = [
    path('pagamento/',pagamento),
    path('pedidos/',dashboard),
    path('ver_pedido/<int:id>/', verPedido),
    path('meu_carrinho/',ver_carrinho),
    path('',cardapio),
    path('<str:mesa>/<str:restaurante>/<int:id>/',cardapio_carrinho),
    path('super_categoria/<str:super_categoria>/',categoria_cookie),
    
    
]