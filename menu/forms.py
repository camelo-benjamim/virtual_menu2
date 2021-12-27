from typing import Text
from django import forms
from django.shortcuts import get_object_or_404
from menu.models import *

### CLASSIFICAÇAO DOS ITENS
class FormClassificacao(forms.ModelForm):
    class Meta:
        model = Item_classificacao
        fields = ['text']
        labels = {'text':('Categoria: ')}
        help_texts = {'text': ('Ex: Petiscos')}
        
### ITENS
class FormItens(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = ['item_nome','classificacao','componentes','descricao','preco','img']
        labels = {'item_nome':('Nome do item: '), 'classificacao':('Classificação: '),'componentes':('Componentes: '),'descricao':('Descrição:'),'preco':('Preco:'),'img':('Imagem do produto')}
    
## FORMULÁRIO PARA EDIÇAO DE ITENS  
class FormEditItens(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = ['item_nome','classificacao','componentes','descricao','preco','img']
        labels = {'item_nome':('Nome do item: '), 'classificacao':('Classificação: '),'componentes':('Componentes: '),'descricao':('Descrição:'),'preco':('Preco:'),'img':('Imagem do produto')}
     
    


        

        