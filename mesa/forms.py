from typing import Text
from django import forms
from mesa.models import *

###FORMULÁRIO PARA ADICIONAR MESA
class FormMesa(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['description']
        labels = {'description': ('Identificação: ')}