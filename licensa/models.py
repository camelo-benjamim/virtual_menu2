from django.db import models
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)


from django_currentuser.db.models import CurrentUserField
from menu.models import Restaurante
# Create your models here.
class Licensa(models.Model):
    usuario_vendedor = CurrentUserField()
    restaurante = models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    meses = models.PositiveSmallIntegerField(default=6)
    data_inicio_licensa = models.DateTimeField(auto_now_add=True,editable=False)
