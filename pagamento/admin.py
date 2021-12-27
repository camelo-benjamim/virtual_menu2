from django.contrib import admin
from pagamento.models import *

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    readonly_fields = ('pagamento',)
    ordering_by = ('id',)
    
    def has_add_permission(self, request, obj=None):
        return False

