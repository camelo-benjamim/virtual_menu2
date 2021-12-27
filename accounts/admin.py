from django.contrib import admin
from accounts.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username','companysname']
    list_filter  = ('postal_code',)
    search_fields = ('companysname',)
    ordering = ('companysname',)
    

##admin.site.register(Group)
admin.site.register(User,CustomUserAdmin)
admin.site.unregister(Group)
admin.site.site_header = "Virtual menu v1.0 "
admin.site.index_title = "Área destinada a manuntenção do site"

