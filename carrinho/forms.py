from django import forms
from carrinho.models import Pedido

class FormPedido(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['item','quantidade']