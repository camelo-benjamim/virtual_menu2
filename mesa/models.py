from django.db import models

## MIDDLEWARE PARA CURRENTUSER
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)


from django_currentuser.db.models import CurrentUserField

# Create your models here.
##MESA DO RESTAURANTE
class Mesa(models.Model):
    ##restaurante = models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    criado_por = CurrentUserField()
    description = models.CharField(max_length=30)

    def __str__(self):
        return str(self.description)
    