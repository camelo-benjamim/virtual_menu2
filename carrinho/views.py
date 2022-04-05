### IMPORTS
from datetime import date, datetime
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
from dateutil.parser import parse
import time


####
def AdicionarNome(request):
    restaurante_id = request.session['restaurante_servidor']
    restaurante = get_object_or_404(Restaurante, id=restaurante_id)
    token_usuario = request.COOKIES[settings.SESSION_COOKIE_NAME]
    carrinho = Cart.objects.filter(session_key=token_usuario)[0]
    if request.method == "POST":
        form = FormNome(request.POST)
        if form.is_valid():
            nome_do_cliente = form.cleaned_data['nome_do_cliente']
            ##PEGANDO PEDIDO ATUAL E ALTERANDO O NOME
            carrinho.nome_do_cliente = nome_do_cliente
            carrinho.save()
            return redirect('/cardapio/pagamento/')
        
    else:
        form = FormNome()
        context = {'form': form,'restaurante': restaurante,}
        
    return render(request,'pedidos/cliente/adicionar_nome.html',context=context)
        
####
def ver_carrinho(request):
    try:
        restaurante_id = request.session['restaurante_servidor']
        restaurante = get_object_or_404(Restaurante, id=restaurante_id)
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
                'carrinho':carrinho, 'pedidos': pedidos, 'valor_total' : valor_total,'quantidade': quantidade, 'restaurante': restaurante,
            }
            return render (request,'pedidos/cliente/carrinho.html',context = context)
        
        else:
            carrinho = get_object_or_404(Cart,concluido=False,session_key=session_key)
            pedidos = carrinho.pedido.all()
            quant_alteracoes = 0
            for pedido in pedidos:
                quantidade = request.POST.get(str(pedido.item))
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
            
            if quant_alteracoes == 0 :
                return redirect('/cardapio/adicionar_nome/')
            else:
                return redirect('/cardapio/meu_carrinho/')
    
    except:
        messages.info(request, 'POR FAVOR, ESCANEIEI O QR CODE PARA QUE O SISTEMA IDENTIFIQUE SUA MESA!')
        return redirect('/cardapio/')

def cardapio_carrinho(request,mesa,restaurante,id):
    restaurante = get_object_or_404(Restaurante,id=id,nome_restaurante=restaurante)
    request.session['restaurante_servidor'] = restaurante.id
    mesa = get_object_or_404(Mesa,description=mesa,restaurante=restaurante)
    try:
        session_key = request.COOKIES[settings.SESSION_COOKIE_NAME]
    except:
        request.session.create()
        session_key = request.session.session_key
        print("iniciando seção")
        request.session['mesa_session'] = mesa.description
        print("printando requisição de mesa: ")
        print(request.session['mesa_session'])
        cart = Cart.objects.filter(session_key=session_key,concluido=False)
        print("carrinho aí: ")
        print(cart)
    try:
        cart_print = cart[0]
        cart_print.mesa_pedido = mesa
        cart_print.save()
        print('carrinho print aí: ')
        print(cart_print)
        return redirect('/cardapio/')
    except:
        novo_carrinho = Cart.objects.create(session_key=session_key,mesa_pedido=mesa,concluido=False)
        novo_carrinho.save()
        print("novo carrinho: ")
        print(cart)
        return redirect ('/cardapio/')

def categoria_cookie(request,super_categoria):
    request.session['categoria'] = super_categoria
    return redirect('/')

##CONTÉM ERROS, VERIFICAR E CORRIGIR
def cardapio(request):
    if request.user.is_active == True:
        return redirect('/cardapio/pedidos/')
    else:
        if request.method == "GET":
            try:
                request.session['categoria']
                restaurante_id = request.session['restaurante_servidor']
                restaurante = get_object_or_404(Restaurante, id=restaurante_id)
            except:
                request.session['categoria'] = None
            super_categorias = Classificacoes.objects.filter(restaurante=request.session['restaurante_servidor'])
            if request.session['categoria'] is None:
                super_exibir = super_categorias.first()
            else:
                super_exibir = get_object_or_404(Classificacoes,nome_classificacao=request.session['categoria'])
            categorias = Item_classificacao.objects.filter(classificacao=super_exibir)
            produtos = []
            for cat in categorias:
                produtos_adicionar = Item.objects.filter(classificacao=cat)
                for pr in produtos_adicionar:
                    produtos.append(pr)                
            form = FormPedido()
            try:
                session_key = request.COOKIES[settings.SESSION_COOKIE_NAME]
                produtos2 = Pedido.objects.filter(session_key=session_key,concluido=False)
                quantidade_cart = 0
                for i in produtos2:
                    quantidade_cart += 1
                lista_itens = []
                for i in produtos2:
                    lista_itens.append(i.item.item_nome)

            except:
                lista_itens = []
                quantidade_cart = 0
            print("o restaurante é: ")
            print(restaurante)
            context = {'super_categorias': super_categorias,'categorias':categorias,'produtos':produtos,'form':form, 'quantidade_cart': quantidade_cart,'lista_itens':lista_itens,'restaurante':restaurante,}        
            return render(request,'pedidos/cliente/cardapio.html',context=context)
        else:
            ##ERRO NO MÉTODO POST
            try:
                print('testando o método post')
                item = request.POST.get("item")
                print(item)
                quantidade = request.POST.get("quantidade")
                print(quantidade)
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
                    return redirect('/cardapio/')
                except:
                    ## CASO N EXISTA SERÁ CRIADO UM NOVO PEDIDO
                    try:
                        print("iniciando novo pedido")
                        request.session['mesa_session']
                        print(request.session['mesa_session'])
                        novo_pedido = Pedido.objects.create(item=item_adicionar,quantidade=quantidade,session_key=session_key,concluido=False)
                        novo_pedido.save()
                    except:
                        print("erro geral, tenta descobrir o que é ...:?")
                        pass
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
                        mesa_session = request.session['mesa_session']
                        print(mesa_session)
                        ##PROVÁVEL ERRO
                        restaurante = request.session['restaurante_servidor']
                        mesa = get_object_or_404(Mesa,description=mesa_session,restaurante=restaurante)
                        novo_cart = Cart.objects.create(session_key=session_key,mesa_pedido=mesa)
                        pedido_a_adicionar = Pedido.objects.filter(session_key=session_key,concluido=False)
                        for p in pedido_a_adicionar:
                            novo_cart.pedido.add(p)
                        ##PROCURANDO PELO ERRO
                    return redirect('/cardapio/')
                
            except:
                ## RETORNA O ERRO CASO N EXISTA SESSION KEY PARA O CLIENTE ESCANEAR O QR CODE AO LADO (NA MESA)
                ## ESSE ERRO SERÁ RETORNADO CASO O CLIENTE ENTRE DIRETAMENTE SEM ESCANEAR O QR CODE, O ERRO SERÁ RETORNADO PROPOSITALMENTE...
                messages.info(request, 'POR FAVOR, ESCANEIEI O QR CODE PARA QUE O SISTEMA IDENTIFIQUE SUA MESA!')
                        
                return redirect('/cardapio/')


### ESSA FUNÇAO NAO PRECISA DO TRY E EXCEPT 
### CASO SEJA RESULTADO DE BUSCA ṔOR URL IRÁ RETORNAR ERRO
### CASO SEJA RETORNADA PELO PROPRIO SISTEMA
    ## ELA CONTERÁ CART E SESSION KEY
def pagamento(request):
    restaurante_id = request.session['restaurante_servidor']
    restaurante = get_object_or_404(Restaurante, id=restaurante_id)
    if request.method == "GET":
        mesas = Mesa.objects.filter(restaurante=request.session['restaurante_servidor'])
        metodos_de_pagamento = MetodosDePagamento.objects.filter(restaurante=request.session['restaurante_servidor'])
        session_key = request.COOKIES[settings.SESSION_COOKIE_NAME]
        cart = Cart.objects.filter(session_key=session_key,concluido=False)
        context = {
            'metodos_de_pagamento': metodos_de_pagamento, 'mesas': mesas, 'cart': cart, 'restaurante': restaurante,
        }
        return render (request,'pedidos/cliente/checkout.html',context=context)
    else:
        metodo = request.POST.get("pagamento_metodo")
        metodo_de_pagamento = get_object_or_404(MetodosDePagamento, nome_metodo_de_pagamento=metodo)
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
        return redirect("/cardapio/pos_pedido")
        
        
### DEVIDO A POSSIBILIDADE DE VULNERABILIDADE ELA SÓ É ACESSADA QUANDO USUÁRIO AUTENTICADO
### NAO RETORNA A TELA DE AUTENTICACAO DEVIDO AOS MESMOS MOTIVOS CITADOS ACIMA    


def dashboard(request):
    ##VERIFICAR SE USUÁRIO É PROPRIETÁRIO
    if request.user.is_authenticated: 
        carrinhos_filtro1 = Cart.objects.filter(concluido=True,finalizado=False)
        ###EXCLUINDO O QUE N PERTENCE AO USUARIO DA QUERYSET
        try:
            restaurante = request.session['restaurante']
            restaurante = get_object_or_404(Restaurante, id=restaurante,proprietario=request.user)
            ##VERIFICANDO TOTAL DE RESTAURANTES
            contabilizador_restaurantes = 0
            restaurantes_total = Restaurante.objects.filter(proprietario=request.user)
            for i in restaurantes_total:
                contabilizador_restaurantes += 1
        except:
            return redirect ('/escolher_restaurante/')
        mesas = Mesa.objects.filter(restaurante=restaurante)
        carrinhos = []
        for i in carrinhos_filtro1:
            if i.mesa_pedido in mesas:
                carrinhos.append(i)
        contador = 0
        for carrinho in carrinhos:
            print(carrinhos[contador])
            contador += 1
            
                
            
        ## RESOLVER MILLESECOUNDS
        context = {
            'total': str(contador), 'carrinhos': carrinhos, 'restaurante': restaurante,'contabilizador_restaurantes': str(contabilizador_restaurantes)
        }
        return render(request,'pedidos/usuario/dashboard.html',context=context)
    
    else:
        return redirect ('/auth/user/login/')
    
    

### VER PEDIDOS INDIVIDUALMENTE
@login_required
def verPedido(request,id):
    restaurante = request.session['restaurante']
    restaurante = get_object_or_404(Restaurante, id=restaurante,proprietario=request.user)
    if request.method == "GET":
    ##EXIBE O PEDIDO DO CLIENTE MOSTRANDO TODOS OS ITENS PEDIDOS PELO CLIENTE...
        ##PROCURAR POSSÍVEIS FALHAS DE SEGURANÇA
        pedido = Cart.objects.filter(id=id)[0]
        conteudo = pedido.pedido.all()
        valor_total = 0
        for i in conteudo:
            valor_total += i.item.preco * i.quantidade
            
        
        context = {'pedido': pedido,'valor_total': valor_total,'restaurante': restaurante,}
        return render(request,'pedidos/usuario/ver_pedido_individualmente.html',context=context)
    
    else:
        ## ALTERA O ESTADO PARA FINALIZADO == TRUE
        pedido = Cart.objects.filter(id=id)[0]
        pedido.finalizado = True
        pedido.save()
        return redirect ('/cardapio/pedidos/')


##ADICIONAR ELEMENTOS A FUNÇÃO
##USUÁRIO PASSA NOME PARA FAZER O PEDIDO


def posPedido(request):
    restaurante_id = request.session['restaurante_servidor']
    restaurante = get_object_or_404(Restaurante, id=restaurante_id)
    context = {
        'restaurante': restaurante,
    }
    return render (request,'pedidos/cliente/aguardando_processamento.html',context=context)