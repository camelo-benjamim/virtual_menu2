from django import forms
from carrinho.models import Pedido, Cart

class FormPedido(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['item','quantidade']
        
class FormNome(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['nome_do_cliente']
        labels = {'nome_do_cliente':('Por favor, informe o seu nome: '),}
        help_text = {'nome_do_cliente': ('Por favor informe seu nome para prosseguir: ')}