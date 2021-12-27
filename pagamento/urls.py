from django.shortcuts import render
from django.urls import path
from pagamento.views import *
##
urlpatterns = [
    path('metodos_de_pagamento/', verMetodosDePagamento),
    path('adicionar_metodo_de_pagamento/',adicionarMetodoDePagamento),
    path('remover_metodo_de_pagamento/',removeMetodosDePagamento),
    path('remover_metodo_de_pagamento/<str:metodo>/',removerMetodoDePagamento),
    
]                  
    