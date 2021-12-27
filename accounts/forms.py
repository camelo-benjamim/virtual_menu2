from django.contrib.auth import forms
from accounts.models import User
from django.forms import ModelForm

from django.contrib.auth import admin as adm

class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ("companysname","postal_code","city","state","address","district","number_ref","first_name","last_name","email","contacts_phone","main","username","password1","password2")
        labels = {'companysname':('Nome do Restaurante:'), 'postal_code':('Código postal(CEP):'),'city': ('Cidade:'),'state': ('Estado:'),'address':('Endereço:'), 'district': ('Bairro:'),'number_ref':('Número de referencia:'),'first_name':('Nome:'), 'last_name':('Sobrenome:'),'contacts_phone':('Número de telefone:'),'main':('Restaurante sede')}
        help_texts = {'companysname': ('Ex: Restaurante do Pablo'),'address': ('Ex: Rua Francisco Siqueira'),'first_name':('Ex: Bruno Rodrigo'),'last_name':('Campos de Almeida'),'username':('Por favor, use um nome de usuário parecido com o do seu estabelecimento'),'main':("Marque a opção caso seja o restaurante principal, caso seja filial NÃO marque!")}
    
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
    def clean_main(self):
        objs = User.objects.all()
        for obj in objs:
            if obj.main == True and self.cleaned_data['main'] == True:
                 raise forms.ValidationError("Você já possui uma sede, caso queira tornar esse restaurante como sede, atualize os dados da sede atual e desabilite a opção sede.")
        return self.cleaned_data['main']
class UserChangeForm(forms.UserChangeForm):
    password = forms.ReadOnlyPasswordHashField()
    class Meta(forms.UserChangeForm.Meta):
        model = User
        fields = ("companysname","postal_code","city","state","address","district","number_ref","first_name","last_name","email","contacts_phone","username","main")
        labels = {'companysname':('Nome da empresa:'),'cnpj':('CNPJ'), 'postal_code':('CEP:'),'city': ('Cidade:'),'state': ('Estado:'),'address':('Endereço:'), 'district': ('Bairro:'),'number_ref':('Número de referencia:'),'first_name':('Nome:'), 'last_name':('Sobrenome:'),'contacts_phone':('Número de telefone:'),'main':('Sede')}
        help_text = {'main':("Marque a opção caso seja o restaurante principal, caso seja filial NÃO marque!")}
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
