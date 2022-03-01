from django.shortcuts import  get_list_or_404, get_object_or_404, render,redirect
from menu.models import * 
from menu.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages


##CATEGORIAS:

###MOSTRA TODAS AS SUPERCATEGORIAS
@login_required
def menuView(request):
    user_status = get_object_or_404(User, pk=request.user.id)
    boolean_statuses = user_status.main
    categoria = Classificacoes.objects.all()
    quantidade = 0
    for i in categoria:
        quantidade += 1
    context = {
        'categorias' : categoria, 'status': boolean_statuses,'quantidade': quantidade,
    }

    return render(request,'menu/classificacao/menu.html',context=context)

###MOSTRA TODAS AS CATEGORIAS
@login_required
def categoriasView(request,superCat):
    user_status = get_object_or_404(User, pk=request.user.id)
    boolean_statuses = user_status.main
    superClassificacao = get_object_or_404(Classificacoes, nome_classificacao=superCat)
    categoria = Item_classificacao.objects.filter(classificacao=superClassificacao)
    quantidade = 0
    for i in categoria:
        quantidade += 1
    context = {
        'categorias' : categoria, 'status': boolean_statuses,'quantidade': quantidade,
    }

    return render(request,'menu/classificacao/subcategoria.html',context=context)

###CRIAR MÉTODOS E TEMPLATES PARA ADICIONAR,REMOVER E EDITAR SUPERCAT
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
            form = FormClassificacao(request.POST,request.FILES)
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
    
    user_status = get_object_or_404(User, pk=request.user.id)
    boolean_statuses = user_status.main
    if boolean_statuses == True:
        if request.method == "GET":
            form = FormClassificacoes()
            context = {
                'form': form,
                'status': boolean_statuses,
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

    else:
        messages.info(request, 'Seu usuário não possui acesso a edição de dados!')
        return redirect ('/')
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

### ADICIONAR MÉTODOS DE PAGAMENTO



###AJUSTES
def settings(request):
    user_status = get_object_or_404(User, pk=request.user.id)
    boolean_statuses = user_status.main
    context = {'status': boolean_statuses,}
        
    return render(request,'configuracoes_internas/settings.html',context=context)
    



def boas_vindas(request):
    return redirect('/cardapio/')