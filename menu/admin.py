from re import search
from django.contrib import admin
from menu.models import *

@admin.register(Item_classificacao)
class ItemClassicacaoAdmin(admin.ModelAdmin):
    readonly_fields = ('text',)
    ordering_by = ('-id',)
    search_filter = ('text',)
    
    def has_add_permission(self, request, obj=None):
        return False
    
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    ##readonly_fields = ('item_nome','componentes','classificacao','descricao','preco','img')
    ordering_by = ('-id',)
    search_filter = ('item_nome',)
    list_display = ['item_nome','classificacao','preco']

    def has_add_permission(self, request, obj=None):
        return False
    
@admin.register(Classificacoes)
class ClassificacoesAdmin(admin.ModelAdmin):
    search_filter = ('classificacao')
    
    def has_add_permission(self, request, obj=None):
        return False

# Register your models here.
