from django.contrib.auth import forms
from accounts.models import User
from django.forms import ModelForm

from django.contrib.auth import admin as adm

class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ("postal_code","city","state","address","district","number_ref","first_name","last_name","email","avatar",'tipo_de_usuario',"contacts_phone","username","password1","password2")
        labels = { 'postal_code':('Código postal(CEP):'),'city': ('Cidade:'),'state': ('Estado:'),'address':('Endereço:'), 'district': ('Bairro:'),'number_ref':('Número de referencia:'),'first_name':('Nome:'), 'last_name':('Sobrenome:'),'contacts_phone':('Número de telefone:'),'avatar':("Avatar do usuário:")}
        
    
    def clean_postal_code(self):
        data = self.cleaned_data['postal_code']
        cont = len(str(data))
        if not cont == 8:
            raise forms.ValidationError("Um cep necessita de  8 dígitos, por favor tente novamente, ele possui " + str(cont))
        return data
    def clean_contacts_phone(self):
        data = self.cleaned_data['contacts_phone']
        cont = len(str(data))
        if not cont == 11:
            raise forms.ValidationError("Por favor digite um número de telefone válido ex: (DDD) 999999999, o número digitado possui " + str(cont))
        return data
class UserChangeForm(forms.UserChangeForm):
    password = forms.ReadOnlyPasswordHashField()
    class Meta(forms.UserChangeForm.Meta):
        model = User
        fields = ("postal_code","city","state","address","district","number_ref","first_name","last_name","email","contacts_phone","avatar","tipo_de_usuario","username")
        labels = {'postal_code':('CEP:'),'city': ('Cidade:'),'state': ('Estado:'),'address':('Endereço:'), 'district': ('Bairro:'),'number_ref':('Número de referencia:'),'first_name':('Nome:'), 'last_name':('Sobrenome:'),'contacts_phone':('Número de telefone:'),'avatar':('Avatar: '),'tipo_de_usuario':('Tipo de usuário: '),}
        def clean_password(self):
            return self.initial["password"]
   
    def clean_postal_code(self):
        data = self.cleaned_data['postal_code']
        cont = len(str(data))
        if not cont == 8:
            raise forms.ValidationError("Um cep necessita de  8 dígitos, por favor tente novamente, ele possui " + str(cont))
        return data
    def clean_contacts_phone(self):
        data = self.cleaned_data['contacts_phone']
        cont = len(str(data))
        if not cont == 11:
            raise forms.ValidationError("Por favor digite um número de telefone válido ex: (DDD) 999999999, o número digitado possui " + str(cont))
        return data


class UserDeleteForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']
