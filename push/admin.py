from django.contrib import admin
from push.models import *
# Register your models here.

@admin.register(Connect)
class ConnectAdmin(admin.ModelAdmin):
    list_display = ('connection_token','link_encurtado','user')
    readonly_fields = ('user',)
    
    def has_add_permission(self, request, obj=None):
        return False
    def has_edit_permission(self,request,obj=None):
        return True
    def has_delete_permission(self,request,obj=None):
        return True