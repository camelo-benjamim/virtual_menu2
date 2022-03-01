from django.shortcuts import redirect, render
from push.forms import Conectar
from push.models import Connect
from django.contrib import messages
from pushbullet import Pushbullet
# Create your views here.
def CreateConnection(request):
        if request.method == "GET":
             form = Conectar()
             context = {
                 'form': form,
             }
             return render(request,'push/add_connection.html',context=context)
        else:
            form = Conectar(request.POST)
            var0 = Connect.objects.filter(user=request.user)
            var1 = []
            for i in var0:
                var1.append(i)
            if var1 == []:
                if form.is_valid():
                    form.user = request.user
                    form.save()
                    return redirect('../test_message/ok/')
                ## test references
                
            else:
                context = {'form': form,}
                ##return to add connection token
                print("o token n foi aceito")
                messages.info(request, 'JÁ EXISTE UM TOKEN, CASO DESEJE CONTINUAR ENTRE NO ADMIN E REMOVA MANUALMENTE')
                return render(request,'push/add_connection.html',context=context)

def TestMessage(request,message):
    token_access = Connect.objects.all().first()
    API_KEY = token_access.connection_token
    
    pb = Pushbullet(API_KEY)
    push = pb.push_note("Testando 123...",message)
    print(push)
    return redirect('/')

def explain(request):
    elements = Connect.objects.all()
    quant = 0
    for i in elements:
        quant+=1
    if quant == 0:
        context = {'instalation' : 'inexistente'}
    else: 
        context = {'instalation': 'existente'}
        
    return render(request,'push/index.html',context=context)