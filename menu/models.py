from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from accounts.models import User
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)


from django_currentuser.db.models import CurrentUserField

##CLASSIFICAÇÃO DO PRODUTO NO CARDÁPIO, EX: BEBIDAS, APERITIVOS E ETC ...
class Restaurante(models.Model):
    nome_restaurante = models.CharField(max_length= 125)
    proprietario = models.ForeignKey(User,on_delete=models.CASCADE,related_name='proprietario_restaurante')
    usuario_criador = CurrentUserField()
    logo_restaurante = models.ImageField(upload_to='logo_restaurantes/')

    def __str__(self):
        return self.nome_restaurante

class Classificacoes(models.Model):
    ##UNIQUE CONSTANT NÃO É APLICADO, USAREI AS VIEWS PARA NÃO PERMITIR ITENS DUPLICADOS
    nome_classificacao= models.CharField(max_length=50)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Classificação"
        verbose_name_plural = "Classificações"
    def __str__(self):
        return self.nome_classificacao
    
class Item_classificacao(models.Model):
    text = models.CharField(max_length=40)
    classificacao = models.ForeignKey(Classificacoes,on_delete=models.CASCADE,default=None)
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        
    def __str__(self):
        return self.text
##ITEM É O PRODUTO EM SÍ QUE APARECERÁ NO CARDÁPIO
class Item(models.Model):
    item_nome = models.CharField(max_length=40)
    classificacao = models.ForeignKey(Item_classificacao,on_delete=models.CASCADE,default=None)
    preco = models.DecimalField(decimal_places=2,max_digits=10)
    img = models.ImageField(upload_to = 'images/',null=True,blank=True, default=None)
    class Meta:
        verbose_name_plural = "Itens"
    def __str__(self):
        return self.item_nome


    
