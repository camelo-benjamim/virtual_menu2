from typing import Text
from django import forms
from django.shortcuts import get_object_or_404
from menu.models import *
from accounts.models import User

### CLASSIFICAÇAO DOS ITENS

class FormClassificacoes(forms.ModelForm):
    class Meta:
        model = Classificacoes
        fields = ['nome_classificacao',]
        labels = {'nome_classificacao':('Ex: Petiscos ')}
class FormClassificacao(forms.ModelForm):
    def __init__(self, restaurante, *args, **kwargs): 
            super(FormClassificacao, self).__init__(*args, **kwargs)
            restaurante_query = get_object_or_404(Restaurante, id=restaurante)
            classificacoes = Classificacoes.objects.filter(restaurante=restaurante_query)
            self.fields['classificacao'].queryset = classificacoes
                     
    class Meta:
        model = Item_classificacao
        fields = ['text','classificacao']
        labels = {'text':('Categoria: '),'classificacao':('Classificação: ')}
        help_texts = {'text': ('Ex: Petiscos')}
        
### ITENS
class FormItens(forms.ModelForm):
    def __init__(self, classificacao,*args, **kwargs): 
            super(FormItens, self).__init__(*args, **kwargs)
            queryset_classificacao = Item_classificacao.objects.filter(id=classificacao)
            super_classificacao_id = queryset_classificacao[0].classificacao.id
            ##pegando obj
            superclassificacao_obj = get_object_or_404(Classificacoes,id=super_classificacao_id)
            irmas = Item_classificacao.objects.filter(classificacao=superclassificacao_obj)
            self.fields['classificacao'].queryset = (queryset_classificacao | irmas).distinct()
    class Meta:
        model = Item
        fields = ['item_nome','classificacao','preco','img']
        labels = {'item_nome':('Nome do item: '), 'classificacao':('Classificação: '),'preco':('Preco:'),'img':('Imagem do produto')}
    
## FORMULÁRIO PARA EDIÇAO DE ITENS  
class FormEditItens(forms.ModelForm):
    def __init__(self, classificacao,*args, **kwargs): 
        super(FormEditItens, self).__init__(*args, **kwargs)
        queryset_classificacao = Item_classificacao.objects.filter(id=classificacao)
        super_classificacao_id = queryset_classificacao[0].classificacao.id
        ##pegando obj
        superclassificacao_obj = get_object_or_404(Classificacoes,id=super_classificacao_id)
        irmas = Item_classificacao.objects.filter(classificacao=superclassificacao_obj)
        self.fields['classificacao'].queryset = (queryset_classificacao | irmas).distinct()
    class Meta:
        model = Item
        fields = ['item_nome','classificacao','preco','img']
        labels = {'item_nome':('Nome do item: '), 'classificacao':('Classificação: '),'preco':('Preco:'),'img':('Imagem do produto')}
     
    

class FormRestaurante(forms.ModelForm):
    def __init__(self, current_user, *args, **kwargs): 
            super(FormRestaurante, self).__init__(*args, **kwargs)
            try:
                queryset_invited = User.objects.filter(codigo_convidado=current_user.codigo_de_convite)
                queryset_my_usr = User.objects.filter(id=current_user.id)
                self.fields['proprietario'].queryset = queryset_invited | queryset_my_usr
            except:
                self.fields['proprietario'].queryset = User.objects.filter(id=current_user.id)
                     
    class Meta:
        model = Restaurante
        fields = ['nome_restaurante','proprietario','logo_restaurante']
        labels = {'nome_restaurante':('Nome do restaurante: '), 'proprietario':('Proprietário'),'logo_restaurante':('Logo do restaurante: ')}
        help_texts = {'proprietario': ('As opções disponíveis são você mesmo e todos os usuários convidados usando seu código de convite... ')}
    
##EDITAR RESTAURANTE
class FormEditRestaurante(forms.ModelForm):
        
    class Meta:
        model = Restaurante
        fields = ['nome_restaurante','logo_restaurante']
        labels = {'nome_restaurante':('Nome do restaurante: ')}
        
    

class FormDeleteRestaurante(forms.ModelForm):
    class Meta:
        model = Restaurante 
        fields = ['nome_restaurante']
        labels = {'nome_restaurante': ('Nome do restaurante: '),}
        