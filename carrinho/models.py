from django.db import models 
from menu.models import Item
from mesa.models import Mesa
from pagamento.models import MetodosDePagamento
from django.conf import settings

# Create your views here.
### MODELO PARA PEDIDO
## A SESSION KEY SERVE PARA IDENTIFICAR O PEDIDO (QUEM O PEDIU)
class Pedido(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    data = models.DateTimeField(auto_now=True)
    session_key = models.TextField()
    concluido = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.quantidade) + ' ' + str(self.item)
 
### MODELO CART SERVE PARA SALVAR O CART
### A SESSION KEY SERVE PARA IDENTIFICAR O PROPRIETÁRIO DO CART    
class Cart(models.Model):
    pedido = models.ManyToManyField(Pedido)
    data_do_pedido = models.TimeField(auto_now_add=True)
    mesa_pedido = models.ForeignKey(Mesa,on_delete= models.CASCADE,null=True)
    metodo_de_pagamento = models.ForeignKey(MetodosDePagamento,on_delete=models.CASCADE,null=True)
    session_key = models.TextField()
    concluido = models.BooleanField(default=False)
    finalizado = models.BooleanField(default=False,null=True)
    pedido_data_relatorio = models.DateField(auto_now_add=True,null=True)
    nome_do_cliente = models.CharField(max_length=120,null=True,default=None)
    class Meta:
        verbose_name = "Carrinho"
        verbose_name_plural = "Carrinhos"

    
    def __str__(self):
        return str(self.session_key)