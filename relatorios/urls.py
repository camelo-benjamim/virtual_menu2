from django.shortcuts import render
from django.urls import path
from relatorios.views import *

urlpatterns = [
    path('',mainRelatorio),
    path('relatorio_dia/',relatorioDia),
    path('relatorio_mes/',relatorioMes),
    path('relatorio_ano/',relatorioAno),
    path("comanda/<int:id_comanda>/",ver_comanda),
]