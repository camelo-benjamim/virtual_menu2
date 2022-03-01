from push.models import Connect
from django import forms

class Conectar(forms.ModelForm):
    class Meta:
        model = Connect
        fields = ["connection_token","link_encurtado"]
        labels = {"connection_token":("Token: "),"link_encurtado":('Link encurtado: ')}
