### IMPORTS
from django.core.checks import messages
from django.shortcuts import get_object_or_404, render,redirect
from carrinho.models import *
from mesa.models import *
from pagamento.models import *
from menu.models import *
from carrinho.forms import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
####


## ESSA FUNÇAO SERVE PARA RETORNAR O CART COM TODOS OS PEDIDOS FEITOS PELO USUÁRIO
### A SESSION KEY JÁ FOI PASSADA PELA FUNCAO ABAIXO DESSA...
### CASO TENTE ACESSAR SEM A SESSION_KEY SERÁ RETORNADO UM ERRO EM FORMA DE ALERT

def ver_carrinho(request):
    try:
        session_key = request.COOKIES[settings.SESSION_COOKIE_NAME]
        if request.method == "GET":
            carrinho = get_object_or_404(Cart,concluido=False,session_key=session_key)
            pedidos = carrinho.pedido.all()
            valor_total = 0
            quantidade = 0
            for q in pedidos:
                quantidade += 1
                
            for pedido_v in pedidos:
                valor_total += pedido_v.item.preco * pedido_v.quantidade
            
            context = {
                'carrinho':carrinho, 'pedidos': pedidos, 'valor_total' : valor_total,'quantidade': quantidade,
            }
            return render (request,'pedidos/cliente/carrinho.html',context = context)
        
        else:
            carrinho = get_object_or_404(Cart,concluido=False,session_key=session_key)
            pedidos = carrinho.pedido.all()
            quant_alteracoes = 0
            for pedido in pedidos:
                print("QUANTIDADE DO PEDIDO:")
                quantidade = request.POST.get(str(pedido.item))
                print(quantidade)
                if not int(quantidade) == pedido.quantidade:
                    ##ALTERAR O PEDIDO
                    quant_alteracoes += 1
                    pedido_a_alterar = Pedido.objects.filter(session_key=session_key,concluido=False,item=pedido.item).first()
                    pedido_a_alterar.quantidade = quantidade
                    pedido_a_alterar.save()
                    
                    
                ###PROCURANDO POR ZEROS 
            pedidos_zerados = Pedido.objects.filter(session_key=session_key,quantidade=0)
            pedidos_zerados.delete()
            ###VERIFICANDO ALTERAÇOES
            
            print("VERIFICANDO....")
            print(quant_alteracoes)
            print(quant_alteracoes)
            if quant_alteracoes == 0 :
                return redirect('/cardapio/pagamento/')
            else:
                return redirect('/cardapio/meu_carrinho/')
    
    except:
        messages.info(request, 'POR FAVOR, ESCANEIEI O QR CODE PARA QUE O SISTEMA IDENTIFIQUE SUA MESA!')
        return redirect('/cardapio/')
        
### ESSA FUNÇAO CRIA UMA  SESSION NO BROWSER CASO A MESMA SEJA INEXISTENTE
### ELA IRÁ CRIAR UM CART CONFORME O QRCODE DA MESA QUE SERÁ PASSADO NA URL 
### O LINK SERÁ DADO PELO QRCODE NA PLACA
def cardapio_carrinho(request,mesa):
    mesa = get_object_or_404(Mesa,description=mesa)
    try:
        session_key = request.COOKIES[settings.SESSION_COOKIE_NAME]
    except:
        request.session.create()
    session_key = request.session.session_key
    print("PRINTANDO A SESSAO NOVA")
    print(session_key)
    print("SESSAO ACIMA")
    cart = Cart.objects.filter(session_key=session_key,concluido=False)
    try:
        ##FORÇAR O ERRO
        cart_print = cart[0]
        print()
        ##ADICIONAR MESA CARTAO
        cart_print.mesa_pedido = mesa
        cart_print.save()
        return redirect('/cardapio/')
    except:
        novo_carrinho = Cart.objects.create(session_key=session_key,mesa_pedido=mesa,concluido=False)
        novo_carrinho.save()
        return redirect ('/cardapio/')
    

##RETORNAR O CARDÁPIO PARA O CLIENTE 
### escolher itens e a quantidade dos mesmos
def cardapio(request):
    if request.method == "GET":
        categorias = Item_classificacao.objects.all()
        produtos = Item.objects.all()
        form = FormPedido()
        try:
            session_key = request.COOKIES[settings.SESSION_COOKIE_NAME]
            produtos2 = Pedido.objects.filter(session_key=session_key,concluido=False)
            quantidade_cart = 0
            for i in produtos2:
                quantidade_cart += 1
                
        except:
            print("DEU ERRO CABRA")
            quantidade_cart = 0
        context = {'categorias':categorias,'produtos':produtos,'form':form, 'quantidade_cart': quantidade_cart,}        
        return render(request,'pedidos/cliente/cardapio.html',context=context)
    else:
        try:
            ##VERIFICA SE EXISTE SESSION KEY
            ### CASO N EXISTA SERÁ RETORNADO UM ERRO NA FORMA DE ALERT 
            item = request.POST.get("item")
            quantidade = request.POST.get("quantidade")
            session_key = request.COOKIES[settings.SESSION_COOKIE_NAME]
            item_adicionar = get_object_or_404(Item,item_nome=item)
            try:
                ### VERIFICA EXISTENCIA DO PEDIDO FEITO
                ## CASO EXISTA SERÁ ADICIONADO A QUANTIDADE A MAIS
                pedido_exist = get_object_or_404(Pedido, item = item_adicionar, session_key = session_key,concluido=False)
                print(pedido_exist)
                quantidade_anterior = pedido_exist.quantidade
                nova_quantidade = int(quantidade_anterior) + int(quantidade)
                pedido_exist.quantidade = nova_quantidade
                pedido_exist.save()
                print(str(nova_quantidade))
                return redirect('/cardapio/')
            except:
                ## CASO N EXISTA SERÁ CRIADO UM NOVO PEDIDO
                novo_pedido = Pedido.objects.create(item=item_adicionar,quantidade=quantidade,session_key=session_key,concluido=False)
                novo_pedido.save()
                
                ### VERIFICA A EXISTENCIA DE UM CART
                ## CASO N EXISTA UM CART O PRODUTO SERÁ CRIADO PORÉM SERÁ DELETAADO AUTOMATICAMENTE
                cart = Cart.objects.filter(session_key=session_key,concluido=False)
                try:
                    if cart[0]:
                        ## SALVANDO OBJETO PEDIDO NO CART
                        pedido_para_salvar = Pedido.objects.filter(session_key=session_key,item=item_adicionar,concluido=False).first()
                        carrinho = get_object_or_404(Cart,session_key=session_key,concluido=False)
                        carrinho.pedido.add(pedido_para_salvar)
                        carrinho.save()
                        print(carrinho)
                        return redirect('/cardapio/')
                        
                ## CASO N EXISTA UM CART, SERÁ RETORNADO A ESSA FUNÇAO QUE DELETA O PEDIDO (CASO N EXISTA UM CART)     
                except:
                    pedido_a_deletar = Pedido.objects.filter(session_key=session_key,item=item_adicionar,concluido=False)
                    for p in pedido_a_deletar:
                        p.delete()
                    
                    ## RETORNA PARA ESCANEAR O QR CODE
                    messages.info(request, 'POR FAVOR, ESCANEIEI O QR CODE PARA QUE O SISTEMA IDENTIFIQUE SUA MESA!')
                    
                return redirect('/cardapio/')
            
        except:
            ## RETORNA O ERRO CASO N EXISTA SESSION KEY PARA O CLIENTE ESCANEAR O QR CODE AO LADO (NA MESA)
            messages.info(request, 'POR FAVOR, ESCANEIEI O QR CODE PARA QUE O SISTEMA IDENTIFIQUE SUA MESA!')
                    
            return redirect('/cardapio/')


### ESSA FUNÇAO NAO PRECISA DO TRY E EXCEPT 
### CASO SEJA RESULTADO DE BUSCA ṔOR URL IRÁ RETORNAR ERRO
### CASO SEJA RETORNADA PELO PROPRIO SISTEMA
    ## ELA CONTERÁ CART E SESSION KEY
def pagamento(request):
    if request.method == "GET":
        mesas = Mesa.objects.all()
        metodos_de_pagamento = Pagamento.objects.all()
        session_key = request.COOKIES[settings.SESSION_COOKIE_NAME]
        cart = Cart.objects.filter(session_key=session_key,concluido=False)
        context = {
            'metodos_de_pagamento': metodos_de_pagamento, 'mesas': mesas, 'cart': cart,
        }
        return render (request,'pedidos/cliente/checkout.html',context=context)
    else:
        metodo = request.POST.get("pagamento_metodo")
        metodo_de_pagamento = get_object_or_404(Pagamento, pagamento=metodo)
        session_key = request.COOKIES[settings.SESSION_COOKIE_NAME]
        cart = Cart.objects.filter(session_key=session_key,concluido=False)
        for i in cart[0].pedido.all():
            item_instance = get_object_or_404(Item, item_nome=i.item)
            pedido_atualizar = Pedido.objects.filter(session_key=session_key,concluido=False,item=item_instance).first()
            pedido_atualizar.concluido = True
            pedido_atualizar.save()
            
        alterar = cart[0]
        alterar.metodo_de_pagamento = metodo_de_pagamento
        alterar.concluido = True
        alterar.save()
        
        return render (request,'pedidos/cliente/aguardando_processamento.html')
        
        
### DEVIDO A POSSIBILIDADE DE VULNERABILIDADE ELA SÓ É ACESSADA QUANDO USUÁRIO AUTENTICADO
### NAO RETORNA A TELA DE AUTENTICACAO DEVIDO AOS MESMOS MOTIVOS CITADOS ACIMA    
@login_required
def dashboard(request):
    carrinhos_filtro1 = Cart.objects.filter(concluido=True,finalizado=False)
    ###EXCLUINDO O QUE N PERTENCE AO USUARIO DA QUERYSET
    mesas = Mesa.objects.filter(criado_por=request.user)
    carrinhos = []
    for i in carrinhos_filtro1:
        if i.mesa_pedido in mesas:
            carrinhos.append(i)
    
    contador = 0
    for carrinho in carrinhos:
        print(carrinhos[contador])
        contador += 1
    
    
    context = {
        'total': str(contador), 'carrinhos': carrinhos,
    }
    return render(request,'pedidos/usuario/dashboard.html',context=context)
    
    
    

### VER PEDIDOS INDIVIDUALMENTE

def verPedido(request,id):
    if request.method == "GET":
    ##EXIBE O PEDIDO DO CLIENTE MOSTRANDO TODOS OS ITENS PEDIDOS PELO CLIENTE...
        pedido = Cart.objects.filter(id=id)[0]
        conteudo = pedido.pedido.all()
        valor_total = 0
        for i in conteudo:
            valor_total += i.item.preco * i.quantidade
            
        
        context = {'pedido': pedido,'valor_total': valor_total,}
        return render(request,'pedidos/usuario/ver_pedido_individualmente.html',context=context)
    
    else:
        ## ALTERA O ESTADO PARA FINALIZADO == TRUE
        pedido = Cart.objects.filter(id=id)[0]
        pedido.finalizado = True
        pedido.save()
        return redirect ('/cardapio/pedidos/')


### VERIFICADO
### FUNCIONANDO CORRETAMENTE
## NAO APRESENTOU ERROS
