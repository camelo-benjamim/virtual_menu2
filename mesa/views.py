from django.shortcuts import  get_list_or_404, get_object_or_404, render,redirect
from mesa.models import * 
from mesa.forms import *
from menu.models import Restaurante
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
###VER MESAS
@login_required
def verMesas(request):
    ##mecanismo de segurança anti-fraude nos cookies sendo passado nas views
    ##verificando se usuário é proprietário do restaurante abaixo:
    try:
        restaurante = get_object_or_404(Restaurante,id=request.session['restaurante'],proprietario=request.user)
    except:
        ##verificando se usuário é usuário criador do restaurante: 
        restaurante = get_object_or_404(Restaurante,id=request.session['restaurante'],usuario_criador=request.user)
    mesas = Mesa.objects.filter(restaurante=restaurante)
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
            exist_condition = Mesa.objects.filter(restaurante=request.session['restaurante'],description=form.cleaned_data['description']).exists()
            if exist_condition == False:
                ## mecanismo de segurança, conforme é explicada em uma view logo mais abaixo:
                ## verificando se é proprietário do restaurante
                try:
                    restaurante = get_object_or_404(Restaurante,id=request.session['restaurante'],proprietario=request.user)
                except:
                    ##verificando se é usuário criador
                    restaurante = get_object_or_404(Restaurante,id=request.session['restaurante'],usuario_criador=request.user)
                
                Mesa.objects.create(restaurante=restaurante, description=form.cleaned_data['description'])
                return redirect ('/settings/')
            else: 
                context = {'form':form,}
                messages.info(request, 'Voce já adicionou uma mesa com o mesmo nome')
                return render(request,'configuracoes_internas/mesas/mesa_add.html',context=context)
        context = {
            'form': form,
        }
        return render (request,'configuracoes_internas/mesas/mesa_add.html',context=context)
## DELETAR MESA
def deleteMesa(request,description):
    try:
        ## Mecanismo de segurança contra alteração de cookies
            ## Em caso de tentativa de requisitar acesso a um restaurante onde não se é criador nem proprietário
        ##verificando se é proprietário
        restaurante = get_object_or_404(Restaurante,proprietario=request.user,id=request.session['restaurante'])
    except:
        ##verificando se é usuário criador
        restaurante = get_object_or_404(Restaurante,usuario_criador=request.user,id=request.session['restaurante'])
    description = get_object_or_404(Mesa, restaurante=restaurante, description = description).delete()
    return redirect ('/settings/')

## VIEW PARA ACESSAR DELETAR MESA
def mesaConsult(request):
    ##Mecanismo anti-fraude
    restaurante = request.session['restaurante']
    try:
        ##verificando se é proprietário
        restaurante_obj = get_object_or_404(Restaurante,id=restaurante,proprietario=request.user)
    except:
        ##verificando se é usuário criador 
        restaurante_obj = get_object_or_404(Restaurante,id=restaurante, proprietario=request.user)
    mesas = Mesa.objects.filter(restaurante=restaurante_obj)
    quantidade = 0
    for i in mesas:
        quantidade += 1
    context = {
            'mesas': mesas, 'quantidade': quantidade,
    }
    return render(request,'configuracoes_internas/mesas/mesa_consult.html', context=context)
