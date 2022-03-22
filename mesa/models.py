from django.db import models
from menu.models import Restaurante

# Create your models here.
##MESA DO RESTAURANTE
##remover o criado por, pois foi substituído por restaurante
class Mesa(models.Model):
    ##restaurante = models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    
    description = models.CharField(max_length=30)
    restaurante = models.ForeignKey(Restaurante,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.description)
    