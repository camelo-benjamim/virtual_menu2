from django.db import models
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)


from django_currentuser.db.models import CurrentUserField

# Create your models here.
class Connect(models.Model):
    connection_token = models.CharField(max_length=200)
    link_encurtado = models.CharField(max_length=50,null=True)
    user = CurrentUserField()
    
    def __str__(self):
        return self.link_encurtado