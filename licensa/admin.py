from django.contrib import admin
from licensa.models import Licensa
# Register your models here.
@admin.register(Licensa)
class LicensaAdmin(admin.ModelAdmin):
    search_fields = ('restaurante',)
    list_display = ('usuario_vendedor','restaurante','meses','data_inicio_licensa', 'data_expiracao','verificado',)
    ##readonly_fields = ('usuario_vendedor','restaurante','meses','data_inicio_licensa')
    def has_add_permission(self, request, obj=None):
        return True
    
