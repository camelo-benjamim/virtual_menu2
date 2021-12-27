from django.shortcuts import render
from django.urls import path
from carrinho.views import *

urlpatterns = [
    path('pagamento/',pagamento),
    path('pedidos/',dashboard),
    path('ver_pedido/<int:id>/', verPedido),
    path('meu_carrinho/',ver_carrinho),
    path('',cardapio),
    path('<str:mesa>/',cardapio_carrinho),
    
    
    
]