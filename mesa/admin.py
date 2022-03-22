from django.contrib import admin
from mesa.models import *

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    search_fields = ('description',)
    list_display = ('description','restaurante')
    readonly_fields = ('restaurante','description')
    
    def has_add_permission(self, request, obj=None):
        return False
    

    
