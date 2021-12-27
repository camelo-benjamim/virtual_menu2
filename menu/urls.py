from django.shortcuts import render
from django.urls import path
from menu.views import *
##
urlpatterns = [
    ## VIEWS DO USUÁRIO
    ###CATEGORIAS
    path('meus_produtos/',menuView, name='adm_view'),
    path('adicionar_categoria/',addCategoria),
    path('remover_categoria/<str:categoria>/',deleteCategoria),
    path('editar_categoria/<str:categoria>/', updateCategoria),
    ###PRODUTOS
    ### VIEWS DE PRODUTOS
    path('produtos_por_categoria/<str:categoria>/',filtrarPorCategoria),
    path('adicionar_produto/',adicionarProduto),
    path('editar_produto/<str:produto>/',editarProduto),
    path('apagar_produto/<str:produto>/',apagarProduto),
    
    ###CONFIGURAÇÕES
    path('settings/',settings),
    path('',boas_vindas,)

    
    
]                  