from django.contrib import admin
from mesa.models import *

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    search_fields = ('description',)
    list_display = ('description','criado_por')
    readonly_fields = ('criado_por','description')
    
    def has_add_permission(self, request, obj=None):
        return False
    

    
