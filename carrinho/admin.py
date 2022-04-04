from django.contrib import admin

from carrinho.models import *

# Register your models here.
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    readonly_fields = ('item','quantidade','session_key','concluido',)
    list_display = ['item','quantidade','concluido']
    list_filter  = ('concluido','item',)
    ordering = ('-id',)
    
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    readonly_fields = ('data_do_pedido','pedido','mesa_pedido','metodo_de_pagamento','session_key','concluido','finalizado','nome_do_cliente')
    list_display = ('mesa_pedido','metodo_de_pagamento','concluido','finalizado',)
    list_filter = ('concluido','finalizado','mesa_pedido',)
    
    def has_add_permission(self, request, obj=None):
        return False