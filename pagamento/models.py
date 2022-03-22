from menu.models import Restaurante
from django.db import models


# Create your models here.
##FORMA DE PAGAMENTOS ACEITAS PELO RESTAURANTE
class Pagamento(models.Model):
    pagamento = models.CharField(max_length=30,unique=True)
    def __str__(self):
        return self.pagamento

class MetodosDePagamento(models.Model):
    restaurante = models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    metodos_aceitos = models.ManyToManyField(Pagamento)