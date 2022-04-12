from django.db import models
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)


from django_currentuser.db.models import CurrentUserField
from menu.models import Restaurante
##
from datetime import timedelta as td, datetime as dt
# Create your models here

##SINCRONIZAR COM API DO COBRE FÁCIL...
class Licensa(models.Model):
    usuario_vendedor = CurrentUserField()
    restaurante = models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    meses = models.PositiveSmallIntegerField(default=6)
    data_inicio_licensa = models.DateTimeField(auto_now_add=True,editable=False)
    verificado = models.BooleanField(default=False)
    @property
    def calcular_data_expiracao(self):
        data_expiracao = dt.now() + td(days=31 * self.meses)
        return data_expiracao
    data_expiracao = calcular_data_expiracao
       
    
    

##TERCEIRIZAR COM API DO COBRE FÁCIL 
##PROVAVELMENTE DISPONÍVEL EM PYTHON
