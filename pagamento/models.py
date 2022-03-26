from menu.models import Restaurante
from django.db import models


# Create your models here.
##FORMA DE PAGAMENTOS ACEITAS PELO RESTAURANTE

class MetodosDePagamento(models.Model):
    restaurante = models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    nome_metodo_de_pagamento = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nome_metodo_de_pagamento