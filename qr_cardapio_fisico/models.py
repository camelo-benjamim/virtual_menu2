from pdb import Restart
from django.db import models
from menu.models import Restaurante
# Create your models here.
class Material(models.Model):
    nome_material = models.CharField(max_length=80,unique=True)
    descricao = models.TextField(null=True,blank=True,default=None)
    valor_unidade = models.DecimalField(decimal_places=2,max_digits=5)
    
class SolicitacaoCardapio(models.Model):
    restaurante = models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    gerar_completo = models.BooleanField(default=True)
    data_pedido = models.DateTimeField(auto_now_add=True)
    material = models.ForeignKey(Material,on_delete=models.CASCADE)
    finalizado = models.BooleanField(default=False)
    
class ServicoOrdem(models.Model):
    soliticatacao = models.ForeignKey(SolicitacaoCardapio,on_delete=models.CASCADE)
    nome_placa = models.CharField(max_length=50)
    url_placa = models.URLField()
    