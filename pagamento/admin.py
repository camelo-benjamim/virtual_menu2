from django.contrib import admin
from pagamento.models import *

@admin.register(MetodosDePagamento)
class PagamentoAdmin(admin.ModelAdmin):
    readonly_fields = ('nome_metodo_de_pagamento',)
    ordering_by = ('id',)
    
    def has_add_permission(self, request, obj=None):
        return False

