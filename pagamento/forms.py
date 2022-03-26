from typing import Text
from django import forms
from django.shortcuts import get_object_or_404
from pagamento.models import *

###formulário de Pagamento
class FormPagamento(forms.ModelForm):
    class Meta:
        model = MetodosDePagamento
        fields = ['nome_metodo_de_pagamento']
        labels = {'nome_metodo_de_pagamento':('Metodo de pagamento: ')}
