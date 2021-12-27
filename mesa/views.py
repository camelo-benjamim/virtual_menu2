from django.shortcuts import  get_list_or_404, get_object_or_404, render,redirect
from mesa.models import * 
from mesa.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
###VER MESAS
@login_required
def verMesas(request):
    mesas = Mesa.objects.filter(criado_por=request.user)
    quantidade = 0
    for i in mesas:
        quantidade += 1
    context = {
            'mesas': mesas, 'quantidade': quantidade,
    }
    return render(request,'configuracoes_internas/mesas/mesa_view.html', context=context)
## ADICIONAR MESA
def addMesa(request):
    if request.method == "GET":
        form = FormMesa()
        context = {
            'form': form,
        }
        return render (request,'configuracoes_internas/mesas/mesa_add.html',context=context)

    else:
        form = FormMesa(request.POST)
        if form.is_valid():
            exist_condition = Mesa.objects.filter(criado_por=request.user,description=form.cleaned_data['description']).exists()
            if exist_condition == False:
                form.save()
                return redirect ('/settings/')
            else: 
                context = {'form':form,}
                messages.info(request, 'Voce já adicionou uma mesa com o mesmo nome')
                return render(request,'configuracoes_internas/mesas/mesa_add.html',context=context)

## DELETAR MESA
def deleteMesa(request,description):
    description = get_object_or_404(Mesa, criado_por = request.user, description = description).delete()
    return redirect ('/settings/')

## VIEW PARA ACESSAR DELETAR MESA
def mesaConsult(request):
    mesas = Mesa.objects.filter(criado_por=request.user)
    quantidade = 0
    for i in mesas:
        quantidade += 1
    context = {
            'mesas': mesas, 'quantidade': quantidade,
    }
    return render(request,'configuracoes_internas/mesas/mesa_consult.html', context=context)
