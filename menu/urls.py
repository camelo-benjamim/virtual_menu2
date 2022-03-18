from django.shortcuts import render
from django.urls import path
from menu.views import *
##
urlpatterns = [
    ## VIEWS DO USUÁRIO
    ##RESTAURANTE
    path('escolher_restaurante/',restauranteChoose),
    path('restaurante_cookie/<int:restaurante>/',restauranteCookie),
    path('adicionar_restaurante/',adicionarRestaurante),
    path('editar_restaurante/<str:nome_restaurante>/',editarRestaurante),
    path('remover_restaurante/<str:nome_restaurante>/',deletarRestaurante),
    path('restaurante_removido/',restauranteRemovido),
    ###CATEGORIAS
    ##SUPER
    path('meus_produtos/',menuView, name='adm_view'),
    path('adicionar_super_categoria/',addSuperCategoria),
    path('remover_super_categoria/<str:super_categoria>/',deleteSuperCategoria),
    path('editar_super_categoria/<str:super_categoria>/', updateSuperCategoria),
    ##SUB
    path('sub_categoria/<str:superCat>/',categoriasView),
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