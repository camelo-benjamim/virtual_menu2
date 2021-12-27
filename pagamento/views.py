from django.shortcuts import  get_list_or_404, get_object_or_404, render,redirect
from pagamento.models import * 
from pagamento.forms import *
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

### RESTAURANTE ADICIONANDO METODOS DE Pagamento
@login_required
def adicionarMetodoDePagamento(request):
    user_status = get_object_or_404(User, pk=request.user.id)
    boolean_statuses = user_status.main
    if boolean_statuses == True:
        if request.method == "GET":
            form = FormPagamento()
            context = {'form':form,}
            return render(request,'configuracoes_internas/pagamento/add_metodo_pagamento.html',context=context)

        else:
            form = FormPagamento(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect ('/settings/')
            else: 
                context = {'form':form,}
                return render(request,'configuracoes_internas/pagamento/add_metodo_pagamento.html',context=context)
                
    else:
        messages.info(request, 'Seu usuário não possui acesso a edição de dados!')
        return redirect ('/settings/')

### VER TODOS OS MÉTODOS DE Pagamento
@login_required
def verMetodosDePagamento(request):
    user_status = get_object_or_404(User, pk=request.user.id)
    boolean_statuses = user_status.main
    if boolean_statuses == True:
        metodos = Pagamento.objects.all()
        quantidade = 0
        for i in metodos:
            quantidade += 1
        context = {
            'metodos' : metodos, 'status': boolean_statuses, 'quantidade': quantidade,
        }

        return render(request,'configuracoes_internas/pagamento/metodos_de_pagamento.html',context=context)

    else:
        messages.info(request, 'Seu usuário não possui acesso a edição de dados!')
        return redirect ('/settings/')

### REMOVER MÉTODO DE Pagamento

def removeMetodosDePagamento(request):
    user_status = get_object_or_404(User, pk=request.user.id)
    boolean_statuses = user_status.main
    if boolean_statuses == True:
        metodos = Pagamento.objects.all()
        quantidade = 0
        for i in metodos:
            quantidade += 1
        context = {
            'metodos' : metodos, 'status': boolean_statuses, 'quantidade': quantidade,
        }

        return render(request,'configuracoes_internas/pagamento/consult_metodo_pagamento.html',context=context)

    else:
        messages.info(request, 'Seu usuário não possui acesso a edição de dados!')
        return redirect ('/settings/')

### REMOVENDO MÉTODO DE Pagamento 
@login_required
def removerMetodoDePagamento(request,metodo):
    user_status = get_object_or_404(User, pk=request.user.id)
    boolean_statuses = user_status.main
    if boolean_statuses == True:
        metod0 = get_object_or_404(Pagamento, pagamento=metodo).delete()
        return redirect ('/settings/')
    else:
        messages.info(request, 'Seu usuário não possui acesso a edição de dados!')
        return redirect ('/settings/')
    

## CONSULTAR MÉTODOS DE Pagamento
def pagamentoConsut(request):
    metodos = Pagamento.objects.all()
    context = {
        'metodos' : metodos,
    }

    return render(request,'configuracoes_internas/pagamento/consult_metodo_pagamento.html',context=context)
