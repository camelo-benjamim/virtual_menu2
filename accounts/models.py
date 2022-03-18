from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

# Create your models here.
STATE_CHOICES = (
    ('AC', 'ACRE'),
    ('AL','ALAGOAS'),
    ('AM','AMAPÁ'),
    ('AZ', 'AMAZONAS'),
    ('BA', 'BAHIA'),
    ('CE','CEARÁ'),
    ('DF','DISTRITO FEDERAL'),
    ('ES','ESPIRITO SANTO'),
    ('GO','GOIÁS'),
    ('MA','MARANHÃO'),
    ('MT','MATO GROSSO'),
    ('MS', 'MATO GROSSO DO SUL'),
    ('MG','MINAS GERAIS'),
    ('PA','PARÁ'),
    ('PB','PARAÍBA'),
    ('PN','PARANÁ'),
    ('PE','PERNAMBUCO'),
    ('PI','PIAUÍ'),
    ('RJ','RIO DE JANEIRO'),
    ('RN','RIO GRANDE DO NORTE'),
    ('RS','RIO GRANDE DO SUL'),
    ('RO','RONDÔNIA'),
    ('RM','RORAIMA'),
    ('SC', 'SANTA CATARINA'),
    ('SP', 'SÃO PAULO'),
    ('SE','SERGIPE'),
    ('TO','TOCANTINS')  

)
TIPOS_DE_USUARIOS = (
    ('V','Vendedor'),
    ('U','Usuário'),
  
)
class User(AbstractUser):
    
    ##IMPORTAR USR E ADICIONAR OS ATRIBUTOS ABAIXO COMO ATRIBUTOS DO USUÁRIO
    ## PODE SER MODIFICADO PELO ADMIN
    postal_code = models.IntegerField(default=0)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2,choices=STATE_CHOICES)
    address = models.CharField(max_length=40)
    district = models.CharField(max_length=40)
    number_ref = models.SmallIntegerField(default=0)
    contacts_phone = models.BigIntegerField(unique=True,default=0)
    avatar = models.ImageField(null=True,blank=True,default=None,upload_to="avatar/")
    tipo_de_usuario = models.CharField(choices=TIPOS_DE_USUARIOS,max_length=2)
    codigo_de_convite = models.UUIDField(default=uuid.uuid4(),unique=True)
    codigo_convidado = models.CharField(null=True,default=None,max_length=120)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name','last_name','email','postal_code','city','state','address','district','number_ref','contacts_phone','tipo_de_usuario']

    def __str__(self):
        return self.username
    