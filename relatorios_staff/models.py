from django.db import models
from django.db import models
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)


from django_currentuser.db.models import CurrentUserField
# Create your models here
class PixProprietario(models.Model):
    usuario = CurrentUserField()
    nome_completo = models.CharField(max_length=255)
    cpf = models.IntegerField()

class PixKeyCpf(models.Model):
    chave_pix_cpf_pk = models.IntegerField()
    proprietario = models.ForeignKey(PixProprietario,on_delete=models.CASCADE)
    boolean_ativa = models.BooleanField(default=True)
    
class PixKeyTelefone(models.Model):
    chave_pix_phone_pk = models.IntegerField()
    proprietario = models.ForeignKey(PixProprietario,on_delete=models.CASCADE)
    boolean_ativa = models.BooleanField(default=True)
    
class PixKeyEmail(models.Model):
    chave_pix_mail_pk = models.EmailField()
    proprietario = models.ForeignKey(PixProprietario,on_delete=models.CASCADE)
    boolean_ativa = models.BooleanField(default=True)
    
class PixRandomKey(models.Model):
    chave_pix_random_key = models.CharField(max_length=255)
    proprietario = models.ForeignKey(PixProprietario,on_delete=models.CASCADE)
    boolean_ativa = models.BooleanField(default=True)