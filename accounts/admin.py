from django.contrib import admin
from accounts.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username','email','contacts_phone','codigo_de_convite']
    list_filter  = ('postal_code',)
    search_fields = ('email','username',)
    ordering = ('date_joined',)
    readonly_fields = ['username','first_name','last_name','email','postal_code','city','state','address','district','number_ref','contacts_phone','avatar','last_login','is_active','date_joined','user_permissions','groups','tipo_de_usuario','codigo_convidado','codigo_de_convite']
    
    def has_add_permission(self, request,obj=None):
        return False
    def has_edit_permission(self,request,obj=None):
        return True
    def has_delete_permission(self, request,obj=None):
        return True

##admin.site.register(Group)
admin.site.register(User,CustomUserAdmin)
admin.site.unregister(Group)
admin.site.site_header = "Virtual menu v1.0 "
admin.site.index_title = "Área destinada a manuntenção do site"

