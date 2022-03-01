from django.shortcuts import get_object_or_404, render,redirect
from datetime import datetime
from datetime import timedelta
from carrinho.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def mainRelatorio(request):
    return render(request,'relatorios/main.html')
def relatorioDia(request):
    ###
    all_carts = Cart.objects.filter(concluido=True,finalizado=True)
    carts_hoje = []
    for i in all_carts:
        if i.pedido_data_relatorio == datetime.today().date():
            carts_hoje.append(i)
    total_apurado = 0
    total_atendimentos = 0
    pedidos = []
    for i in carts_hoje:
        for pedido in i.pedido.all():
            total_atendimentos += 1
            pedidos.append(pedido)
            total_apurado += pedido.item.preco
            
    context = {'relatorio_diario': carts_hoje,'pedidos':pedidos,'total_apurado':total_apurado,'atendimentos': total_atendimentos,}
    return render(request,'relatorios/relatorio_diario.html',context=context)

@login_required
def relatorioMes(request):
    carts = Cart.objects.filter(concluido=True,finalizado=True)
    today = datetime.today()
    ano_atual =  today.strftime("%Y")
    mes_atual = today.strftime("%m")
    carts_mes = []
    for cart in carts:
        data_cart = cart.pedido_data_relatorio
        cart_ano = data_cart.year
        cart_mes = data_cart.month
        if str(ano_atual) == str(cart_ano) and int(str(mes_atual)) == int(str(cart_mes)):
            carts_mes.append(cart)
    
    atendimentos = 0
    valor_total = 0
    for i in carts_mes:
        atendimentos += 1
        pedidos = i.pedido.all()
        for pedido in pedidos:
            quantidade = pedido.quantidade
            preco = pedido.item.preco
            valor_total += preco * quantidade
            
    
    context = {'relatorio':'Relatório mensal','atendimentos': atendimentos, 'valor_total': valor_total,}    
    return render(request,'relatorios/relatorios.html',context=context)
    
    
@login_required
def relatorioAno(request):
    carts = Cart.objects.filter(concluido=True,finalizado=True)
    today = datetime.today()
    ano_atual =  today.strftime("%Y")
    carts_ano = []
    for cart in carts:
        data_cart = cart.pedido_data_relatorio
        cart_ano = data_cart.year
        
        if str(ano_atual) == str(cart_ano):
            carts_ano.append(cart)
            
    atendimentos = 0
    valor_total = 0
    for i in carts_ano:
        atendimentos += 1
        pedidos = i.pedido.all()
        for pedido in pedidos:
            quantidade = pedido.quantidade
            preco = pedido.item.preco
            valor_total += preco * quantidade

    context = {"relatorio":"Relatório Anual", 'atendimentos': atendimentos, 'valor_total': valor_total,}
    return render(request,'relatorios/relatorios.html',context=context)
    ##funcionando

@login_required
def ver_comanda(request,id_comanda):
    pk_cart = id_comanda
    try:
        cart = get_object_or_404(Cart,pk=pk_cart)
        pedidos = cart.pedido.all()
        hora = cart.data_do_pedido
        data = cart.pedido_data_relatorio
        mesa = cart.mesa_pedido
        metodo_pagamento = cart.metodo_de_pagamento
        valor_total = 0
        for i in pedidos:
            adicionar = i.item.preco
            valor_total += adicionar
        
        context = {'pedidos':pedidos,'hora':hora,'data':data,'mesa':mesa,'metodo_pagamento': metodo_pagamento, 'valor_total': valor_total,}
        return render(request,'relatorios/comanda.html',context=context)
    except:
        ##retornar obj n existe
        error = "Erro, o cart escolhido foi deletado"
        context= {'error': error,}
        return render(request,'relatorios/relatorio_diario.html',context=context)
