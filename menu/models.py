from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from accounts.models import User

##CLASSIFICAÇÃO DO PRODUTO NO CARDÁPIO, EX: BEBIDAS, APERITIVOS E ETC ...
class Item_classificacao(models.Model):
    text = models.CharField(max_length=25,unique=True)
    
    class Meta:
        verbose_name_plural = "Categorias"
        
        
    def __str__(self):
        return self.text


##ITEM É O PRODUTO EM SÍ QUE APARECERÁ NO CARDÁPIO
class Item(models.Model):
    item_nome = models.CharField(max_length=40,unique=True)
    componentes = models.TextField(null=True,blank=True,default=None)
    classificacao = models.ForeignKey(Item_classificacao,on_delete=models.CASCADE,default=None)
    descricao = models.CharField(null=True,default=True,max_length=50)
    preco = models.DecimalField(decimal_places=2,max_digits=10)
    img = models.ImageField(upload_to = 'logo/logo_produtos/',null=True,blank=True, default=None)
    
    class Meta:
        verbose_name_plural = "Itens"
    

    def __str__(self):
        return self.item_nome


    
