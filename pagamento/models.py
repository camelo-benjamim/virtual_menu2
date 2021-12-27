from menu.models import Item
from django.db import models

# Create your models here.
##FORMA DE PAGAMENTOS ACEITAS PELO RESTAURANTE
class Pagamento(models.Model):
    pagamento = models.CharField(max_length=30,unique=True)
    
    def __str__(self):
        return self.pagamento

