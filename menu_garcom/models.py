from email.policy import default
from django.db import models
from menu.models import Item
from mesa.models  import Mesa
from pagamento.models import MetodosDePagamento
# Create your models here.
class PedidoGarçom(models.Model):
    item_pedido = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    
class CarrinhoGarçom(models.Model):
    pedidos = models.ManyToManyField(PedidoGarçom)
    datetime_pedido = models.DateTimeField(auto_now_add=True)
    finalizado = models.BooleanField(default=False)
    mesa_pedido = models.ForeignKey(Mesa,on_delete=models.CASCADE)
    metodo_de_pagamento = models.ForeignKey(MetodosDePagamento,on_delete=models.CASCADE)
    
class DeviceConnection(models.Model):
    session_key = models.TextField()
    codigo_conexao = models.IntegerField()
    validado = models.BooleanField(default=False)

    