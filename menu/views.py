from tracemalloc import get_object_traceback
from django.shortcuts import  get_list_or_404, get_object_or_404, render,redirect
from menu.models import * 
from menu.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

###FUNÇÕES RELACIONADAS A RESTAURANTE

##adiciona restaurante, os proprietários podem ser apenas usuários com seu código de convite
##isso é feito como uma medida de segurança,com a finalidade de evitar fraudes
def adicionarRestaurante(request):
    if request.method == "GET":
        form = FormRestaurante()
        context = {'form': form,}
        return render(request,'restaurante/adicionar_restaurante.html',context=context)  
    else:
        form = FormRestaurante(request.POST,request.FILES)
        if form.is_valid():
            proprietario = form.cleaned_data['proprietario']
            nome = form.cleaned_data['nome_restaurante']
            restaurantes = Restaurante.objects.filter(proprietario=proprietario, nome_restaurante=nome).first()
            if restaurantes == None:
                form.save()
                return redirect("/")
            else:
                messages.info(request, 'Você já adicionou este restaurante anteriormente')
        context = {'form':form,}
        return render(request,'restaurante/adicionar_restaurante.html',context=context)
###concluir
def editarRestaurante(request,nome_restaurante):
    usuario=request.user
    if request.method == "GET":
        try:
            instance = get_object_or_404(Restaurante,nome_restaurante=nome_restaurante, proprietario=usuario)
            ##VERIFICAR PRÉ-EXISTENCIA DE RESTAURANTE COM O MESMO NOME DO MESMO USUÁRIO
            ##EXCLUINDO O ATUAL
        except:
            try:
                instance = get_object_or_404(Restaurante,nome_restaurante=nome_restaurante,usuario_criador=usuario)
            except:
                pass
        
        form = FormRestaurante(instance=instance)
        context = {'form': form,}
        return render(request,'restaurante/editar_restaurante.html',context=context)  
    else:
        form = FormRestaurante(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")
        context = {'form':form,}
        return render(request,'restaurante/editar_restaurante.html',context=context)

##deleta o restaurante
def deletarRestaurante(request,nome_restaurante):
    current_user = request.user
    if request.method == "GET":
        restaurante = get_object_or_404(Restaurante, proprietario=current_user,nome_restaurante=nome_restaurante)
        form = FormDeleteRestaurante()
        context = {
            'form': form,
            'restaurante': restaurante,
        }
    else:
        form = FormDeleteRestaurante(request.POST)
        ## if user = request.user
        try:
            nome_restaurante_form = form['nome_restaurante'].value()
            print(nome_restaurante)
            restaurante = get_object_or_404(Restaurante, proprietario=current_user,nome_restaurante=nome_restaurante_form)
            request.session['restaurante_removido'] = restaurante.nome_restaurante
            restaurante.delete()
            return redirect ('/restaurante/restaurante_removido.html')
        
        except:
            messages.info(request, 'Por favor, digite o nome do restaurante corretamente para prosseguir')
            context={'form': form,}
            return render(request,'restaurante/remover_restaurante.html',context=context)

    return render(request, 'restaurante/remover_restaurante.html',context)
##tela exibida após restaurante ser removido
def restauranteRemovido(request):
    try:
        restaurante_deletado = request.session['restaurante_removido']
        context = {'restaurante_deletado': restaurante_deletado,}
        return render(request, "restaurante/restaurante_deletado.html",context=context)

    except:
        pass

## essa view é para escolher qual restaurante acessar
## no caso de ser usuario e ser proprietário de mais de um restaurante
## e no caso de ser vendedor...
def restauranteChoose(request):
    ##verificando por tipos de usuário
    if request.user.tipo_de_usuario == "U":
        restaurantes = Restaurante.objects.filter(proprietario=request.user)
        context = {'restaurantes': restaurantes,}
    else:
        restaurantes = Restaurante.objects.filter(usuario_criador=request.user)
        context = {'restaurantes':restaurantes,}
    
    return render(request,'restaurante/restaurante_choose.html',context=context)

##view de controle do sistema para passar os cookies com a finalidade de marcar o restaurante escolhido
def restauranteCookie(request,restaurante):
    if request.user.tipo_de_usuario == "U":
        restaurante = get_object_or_404(Restaurante,id=restaurante,proprietario=request.user)
    else:
        restaurante = get_object_or_404(Restaurante,id=restaurante,usuario_criador=request.user)
    
    request.session['restaurante']=restaurante.id
    return redirect('/meus_produtos/')
##CATEGORIAS:

###MOSTRA TODAS AS SUPERCATEGORIAS
@login_required
def menuView(request):
    ##verificando tipo de usuario
    if request.user.tipo_de_usuario == "U":
        try:
            restaurante = get_object_or_404(Restaurante,proprietario=request.user)
            request.session['restaurante']=restaurante.id
        except:
            try:
                restaurante_id = request.session['restaurante']
                mecanismo_seguranca = get_object_or_404(Restaurante,pk=restaurante_id,proprietario=request.user)
                restaurante = mecanismo_seguranca.id
            except:
                return redirect('/escolher_restaurante/')
    ##para o caso de o vendedor acessar os dados do restaurante
    else:
        try:
            restaurante_id = request.session['restaurante']
            mecanismo_seguranca = get_object_or_404(Restaurante,pk=restaurante_id,usuario_criador=request.user)
            restaurante = mecanismo_seguranca.id
        except:
            ##caso ainda não tenha passado pela seleção
            return redirect('/escolher_restaurante/')
    categoria = Classificacoes.objects.filter(restaurante=restaurante)
    quantidade = 0
    for i in categoria:
        quantidade += 1
    context = {
        'categorias' : categoria,'quantidade': quantidade,
    }

    return render(request,'menu/classificacao/menu.html',context=context)

###MOSTRA TODAS AS CATEGORIAS
@login_required
def categoriasView(request,superCat):
    ##verificação de segurança:
    restaurante_cookie = request.sessions['restaurante']
    tipo_usuario = request.user.tipo_de_usuario
    if tipo_usuario == "U":
        restaurante = get_object_or_404(Restaurante,proprietario=request.user,pk=restaurante_cookie)
    else:
        restaurante = get_object_or_404(Restaurante,usuario_criador=request.user,pk=restaurante_cookie)
    superClassificacao = get_object_or_404(Classificacoes, nome_classificacao=superCat,restaurante=restaurante)
    categoria = Item_classificacao.objects.filter(classificacao=superClassificacao)
    quantidade = 0
    for i in categoria:
        quantidade += 1
    context = {
        'categorias' : categoria,'quantidade': quantidade,
    }

    return render(request,'menu/classificacao/subcategoria.html',context=context)

###ADICIONA CATEGORIAS 
@login_required
def addCategoria(request):

    user_status = get_object_or_404(User, pk=request.user.id)
    boolean_statuses = user_status.main
    if boolean_statuses == True:
        if request.method == "GET":
            form = FormClassificacao()
            context = {
                'form': form,
                'status': boolean_statuses,
            }
            return render (request,'menu/classificacao/add_classificacao.html',context=context)
        
        else:
            form = FormClassificacao(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/meus_produtos/')
                
            else:
                context = {'form': form,}
                return render(request,'menu/classificacao/add_classificacao.html',context=context)

    else:
        messages.info(request, 'Seu usuário não possui acesso a edição de dados!')
        return redirect ('/')
    
###ADICIONA SUPERCATEGORIAS 
@login_required
def addSuperCategoria(request):
    ##corrigir formulário e passar o restaurante atual no mesmo
    tipo_usuario = request.user.tipo_de_usuario
    restaurante_cookie = request.session['restaurante']
    if tipo_usuario == "U":
        restaurante = get_object_or_404(Restaurante,pk=restaurante_cookie,proprietario=request.user)
    else:
        restaurante = get_object_or_404(Restaurante,pk=restaurante_cookie,usuario_criador=request.user)
    
    ##metodos
    if request.method == "GET":
        form = FormClassificacoes()
        context = {
            'form': form,
                
        }
        return render (request,'menu/classificacao/add_superclassificacao.html',context=context)
        
    else:
        form = FormClassificacoes(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/meus_produtos/')
                
        else:
            context = {'form': form,}
            return render(request,'menu/classificacao/add_classificacoes.html',context=context)

### DELETAR CATEGORIA
@login_required
def deleteCategoria(request,categoria):
    user_status = get_object_or_404(User, pk=request.user.id)
    boolean_statuses = user_status.main
    if boolean_statuses == True:
        categorias = get_object_or_404(Item_classificacao, text=categoria).delete()
        return redirect ('/meus_produtos/')
    else:
        messages.info(request, 'Seu usuário não possui acesso a edição de dados!')
        return redirect ('/')

### DELETAR SUPERCATEGORIA
@login_required
def deleteSuperCategoria(request,super_categoria):
    user_status = get_object_or_404(User, pk=request.user.id)
    boolean_statuses = user_status.main
    if boolean_statuses == True:
        categorias = get_object_or_404(Classificacoes, nome_classificacao=super_categoria).delete()
        return redirect ('/meus_produtos/')
    else:
        messages.info(request, 'Seu usuário não possui acesso a edição de dados!')
        return redirect ('/')

### ATUALIZAR A CATEGORIA (COM NOVOS VALORES)
@login_required
def updateCategoria(request,categoria):
    user_status = get_object_or_404(User, pk=request.user.id)
    boolean_statuses = user_status.main
    if boolean_statuses == True:
        post = get_object_or_404(Item_classificacao, text=categoria)
        form = FormClassificacao(instance=post)
        if(request.method == 'POST'):
            form = FormClassificacao(request.POST,request.FILES, instance=post)
            if(form.is_valid()):
                    post = form.save(commit=False)
                    post.text = form.cleaned_data['text']
                    post.classificacao = form.cleaned_data['classificacao']
                    post.save()
                    return redirect('/meus_produtos/')
    else:
        messages.info(request, 'Seu usuário não possui acesso a edição de dados!')
        return redirect ('/')
            
            
       
    context = {'form': form,'post':post,}
    return render(request,'menu/classificacao/edit_categoria.html',context=context)
    
###ATUALIZAR SUPER-CATEGORIA
@login_required
def updateSuperCategoria(request,super_categoria):
    user_status = get_object_or_404(User, pk=request.user.id)
    boolean_statuses = user_status.main
    if boolean_statuses == True:
        post = get_object_or_404(Classificacoes, nome_classificacao=super_categoria)
        form = FormClassificacoes(instance=post)
        if(request.method == 'POST'):
            form = FormClassificacoes(request.POST,request.FILES, instance=post)
            if(form.is_valid()):
                    post = form.save(commit=False)
                    post.nome_classificacao = form.cleaned_data['nome_classificacao']
                    post.save()
                    return redirect('/meus_produtos/')
    else:
        messages.info(request, 'Seu usuário não possui acesso a edição de dados!')
        return redirect ('/')
            
            
       
    context = {'form': form,'post':post,}
    return render(request,'menu/classificacao/edit_super_categoria.html',context=context)


###EXIBIR PRODUTOS DE ACORDO COM SUA CATEGORIA
@login_required
def filtrarPorCategoria(request,categoria):
    user_status = get_object_or_404(User, pk=request.user.id)
    boolean_statuses = user_status.main
    categoria_var = Item_classificacao.objects.filter(text=categoria).first()
    
    produtos = Item.objects.filter(classificacao = categoria_var)
    quantidade = 0
    for i in produtos:
        quantidade += 1
    
    context = {
        'produtos': produtos,'status': boolean_statuses,'quantidade':quantidade,
    }
    return render(request,'menu/produtos/produtos_por_categoria.html',context=context)
### ADICIONAR PRODUTO
@login_required
def adicionarProduto(request):
    user_status = get_object_or_404(User, pk=request.user.id)
    boolean_statuses = user_status.main
    if boolean_statuses == True:
        if request.method == 'GET':
            form = FormItens()
            context = {
                'form': form,
            }
            return render(request,'menu/produtos/adicionar_produto.html',context=context)
        else:
            form = FormItens(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect ('/meus_produtos/')
            else: 
                context = {'form':form,}
                return render(request,'menu/produtos/adicionar_produto.html',context=context)
    else:
        messages.info(request, 'Seu usuário não possui acesso a edição de dados!')
        return redirect ('/')

###EDITAR PRODUTO
@login_required
def editarProduto(request,produto):
    user_status = get_object_or_404(User, pk=request.user.id)
    boolean_statuses = user_status.main
    if boolean_statuses == True:
        post = get_object_or_404(Item,item_nome=produto)
        form = FormEditItens(instance=post)
        if(request.method == 'POST'):
            form = FormEditItens(request.POST,request.FILES, instance=post)
            if(form.is_valid()):
                    post = form.save(commit=False)
                    post.item_nome = form.cleaned_data['item_nome']
                    post.classificacao = form.cleaned_data['classificacao']
                    post.descricao = form.cleaned_data['descricao']
                    post.preco = form.cleaned_data['preco']
                    post.img = form.cleaned_data['img']
                    post.save()
                    return redirect('/meus_produtos/')
                
    
        
        context = {'form': form,'post':post,}
        return render(request,'menu/produtos/editar_produto.html',context=context)
    else:
        messages.info(request, 'Seu usuário não possui acesso a edição de dados!')
        return redirect ('/')
            
        

###APAGAR PRODUTO
@login_required
def apagarProduto(request,produto):
    user_status = get_object_or_404(User, pk=request.user.id)
    boolean_statuses = user_status.main
    if boolean_statuses == True:
        produto = get_object_or_404(Item,item_nome = produto).delete()
        return redirect ('/meus_produtos/')
    else:
        messages.info(request, 'Seu usuário não possui acesso a edição de dados!')
        return redirect ('/')

###AJUSTES
@login_required
def settings(request):
    return render(request,'configuracoes_internas/settings.html')

def boas_vindas(request):
    return redirect('/cardapio/')

