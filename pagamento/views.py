from django.shortcuts import  get_list_or_404, get_object_or_404, render,redirect
from pagamento.models import * 
from pagamento.forms import *
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

### RESTAURANTE ADICIONANDO METODOS DE Pagamento
@login_required
def adicionarMetodoDePagamento(request):
    if request.method == "GET":
        form = FormPagamento()
        context = {'form':form,}
        return render(request,'configuracoes_internas/pagamento/add_metodo_pagamento.html',context=context)

    else:
        form = FormPagamento(request.POST, request.FILES)
        restaurante = request.session['restaurante']
        restaurante = get_object_or_404(Restaurante,id=restaurante)
        if form.is_valid():
            ##CRIANDO OBJETO E PASSANDO O RESTAURANTE COMO ARGUMENTO AQUI AO INVÉS DE NOS FORMS
            MetodosDePagamento.objects.create(restaurante=restaurante,nome_metodo_de_pagamento = form.cleaned_data['nome_metodo_de_pagamento'])
            return redirect ('/settings/')
        else: 
            print("formulário inválido")
            context = {'form':form,}
            return render(request,'configuracoes_internas/pagamento/add_metodo_pagamento.html',context=context)

### VER TODOS OS MÉTODOS DE Pagamento
@login_required
def verMetodosDePagamento(request):
    try:
        restaurante = get_object_or_404(Restaurante,pk=request.session['restaurante'])
    except:
        return redirect ('/escolher_restaurante/')
    metodos = MetodosDePagamento.objects.filter(restaurante=restaurante)
    quantidade = 0
    for i in metodos:
        quantidade += 1
    context = {
        'metodos' : metodos,'quantidade': quantidade,
    }

    return render(request,'configuracoes_internas/pagamento/metodos_de_pagamento.html',context=context)

### REMOVER MÉTODO DE Pagamento

def removeMetodosDePagamento(request):
    try:
        restaurante = get_object_or_404(Restaurante,pk=request.session['restaurante'])
    except:
        return redirect ('/escolher_restaurante/')
    
    metodos = MetodosDePagamento.objects.filter(restaurante=restaurante)
    quantidade = 0
    for i in metodos:
        quantidade += 1
    context = {
        'metodos' : metodos, 'quantidade': quantidade,
    }

    return render(request,'configuracoes_internas/pagamento/consult_metodo_pagamento.html',context=context)
### REMOVENDO MÉTODO DE Pagamento 
@login_required
def removerMetodoDePagamento(request,metodo):
    metod0 = get_object_or_404(MetodosDePagamento, nome_metodo_de_pagamento=metodo).delete()
    return redirect ('/settings/')
    

## CONSULTAR MÉTODOS DE Pagamento
def pagamentoConsut(request):
    try:
        restaurante = request.session['restaurante']
        restaurante = get_object_or_404(Restaurante,id=restaurante)
    except:
        return redirect ('/escolher_restaurante/')
    metodos = MetodosDePagamento.objects.filter(restaurante=restaurante)
    context = {
        'metodos' : metodos,
    }

    return render(request,'configuracoes_internas/pagamento/consult_metodo_pagamento.html',context=context)
