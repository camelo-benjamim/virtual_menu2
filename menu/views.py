from tracemalloc import get_object_traceback
from django.shortcuts import  get_list_or_404, get_object_or_404, render,redirect
from menu.models import * 
from menu.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

##Restaurante --> funções (adicionar,editar e remover)
def adicionarRestaurante(request):
    if request.method == "GET":
        form = FormRestaurante(current_user=request.user)
        contador_restaurantes1 = Restaurante.objects.filter(proprietario=request.user)
        contador_restaurantes2 = Restaurante.objects.filter(usuario_criador=request.user)
        contador_geral = 0
        contagem_geral = []
            ##adicionando tudo ...
        for i in contador_restaurantes1:
            if not contagem_geral.__contains__(i):
                contagem_geral.append(i)
        for k in contador_restaurantes2:
            if not contagem_geral.__contains__(k):
                contagem_geral.append(i)
        for j in range(len(contagem_geral)):
            contador_geral +=1
            
        context = {'form': form,'contador_geral': contador_geral,}
        return render(request,'restaurante/adicionar_restaurante.html',context=context)  
    else:
        form = FormRestaurante(request.user,request.POST,request.FILES)
        if form.is_valid():
            proprietario = form.cleaned_data['proprietario']
            nome = form.cleaned_data['nome_restaurante']
            ##verificando se o proprietário já possui um restaurante com esse mesmo nome
            restaurantes = Restaurante.objects.filter(proprietario=proprietario, nome_restaurante=nome).first()
            if restaurantes == None:
                form.save()
                restaurantes_proprietario = Restaurante.objects.filter(proprietario=request.user)
                restaurantes_vendedor = Restaurante.objects.filter(usuario_criador=request.user)
                restaurantes = []
                for i in restaurantes_proprietario:
                    restaurantes.append(i)
                for w in restaurantes_vendedor:
                    if not restaurantes.__contains__(w):
                        restaurantes.append(i)
                if len(restaurantes) > 1:
                    return redirect("/escolher_restaurante/")
                else:
                    restaurante = restaurantes[0]
                    request.session['restaurante'] = restaurante.id
                    return redirect ('/meus_produtos/')
            else:
                messages.info(request, 'Você já adicionou um restaurante para este mesmo proprietário com esse nome, tente novamente com outro nome')
      
            
        context = {'form':form,}
        return render(request,'restaurante/adicionar_restaurante.html',context=context)
###Editar restaurante existente
##ÚNICO BUG NESSA CLASSE
def editarRestaurante(request):
    ##mecanismo de verificação de segurança
    try:
        request.session['restaurante']
    except:
        return redirect ('/escolher_restaurante/')
    try:
        ##verificando se usuário é proprietário
        post = get_object_or_404(Restaurante,id=request.session['restaurante'],proprietario=request.user)
    except:
        ##verificando se usuário é usuário criador
        post = get_object_or_404(Restaurante,id=request.session['restaurante'],usuario_criador=request.user)
    post.proprietario == None
    form = FormEditRestaurante(instance=post)
    if(request.method == 'POST'):
        form = FormEditRestaurante(request.POST,request.FILES, instance=post)
        if(form.is_valid()):
                post.nome_restaurante = form.cleaned_data['nome_restaurante']
                post.logo_restaurante = form.cleaned_data['logo_restaurante']
                post.save()
                return redirect('/escolher_restaurante/')
    
    
    context = {'form':form, post:post,}
    return render(request,'restaurante/editar_restaurante.html',context=context)

    
##deleta o restaurante
def deletarRestaurante(request,nome_restaurante):
    ## o único mecanismo de verificação para essa view é ser proprietário do restaurante
    ## poís o usuário criador NÃO pode deletar o restaurante
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
            restaurante = get_object_or_404(Restaurante, proprietario=current_user,nome_restaurante=nome_restaurante_form)
            ## esse cookie é salvo para printar na próxima tela o nome do restaurante que foi deletado
            request.session['restaurante_removido'] = restaurante.nome_restaurante
            restaurante.delete()
            return redirect ('/restaurante_removido/')
        
        except:
            messages.info(request, 'Por favor, digite o nome do restaurante corretamente para prosseguir')
            context={'form': form,}
            return render(request,'restaurante/remover_restaurante.html',context=context)

    return render(request, 'restaurante/remover_restaurante.html',context)
##tela exibida após restaurante ser removido
def restauranteRemovido(request):
    try:
        ##nesse caso não necessita de confirmação de segurança
        ##pois o request.session (sessão-token) o faz automaticamente
        restaurante_deletado = request.session['restaurante_removido']
        context = {'restaurante_deletado': restaurante_deletado,}
        return render(request, "restaurante/restaurante_deletado.html",context=context)

    except:
        pass

###escolhendo qual restaurante acessar, para o caso de ter mais de um
##caso seja usuário mesmo que tenha apenas um, ele irá o exibir para ser escolhido
def restauranteChoose(request):
    ##verificando por tipos de usuário
    restaurantes_proprietario = Restaurante.objects.filter(proprietario=request.user)
    restaurantes_vendedor = Restaurante.objects.filter(usuario_criador=request.user)
    restaurantes = []
    for i in restaurantes_proprietario:
        restaurantes.append(i)
    for k in restaurantes_vendedor:
        if not restaurantes.__contains__(k):
            restaurantes.append(k)
    
    restaurantes_len = 0
    for w in restaurantes:
        restaurantes_len += 1
    if restaurantes_len >=1:
        context = {'restaurantes': restaurantes,}
        return render(request,'restaurante/restaurante_choose.html',context=context)
    else:
        return redirect('/adicionar_restaurante/')

##view de controle do sistema para passar os cookies com a finalidade de marcar o restaurante escolhido
def restauranteCookie(request,restaurante):
    ##mecanismo de segurança implementado com sucesso
    try:
        restaurante = get_object_or_404(Restaurante,id=restaurante,proprietario=request.user)
    except:
        try:
            restaurante = get_object_or_404(Restaurante,id=restaurante,usuario_criador=request.user)
        except: 
            pass
    request.session['restaurante']=restaurante.id
    return redirect('/meus_produtos/')

##Supercategorias
@login_required
def menuView(request):
    ##verificando tipo de usuario
    try:
       restaurante_id = request.session['restaurante']
       try:
           restaurante = get_object_or_404(Restaurante,id=restaurante_id,proprietario=request.user)
       except:
            restaurante = get_object_or_404(Restaurante,id=restaurante_id,usuario_criador=request.user)
    except:
        return redirect('/escolher_restaurante/')
    categoria = Classificacoes.objects.filter(restaurante=restaurante)
    quantidade = 0
    for i in categoria:
        quantidade += 1
    context = {
        'categorias' : categoria,'quantidade': quantidade,
    }

    return render(request,'menu/classificacao/menu.html',context=context)

##Mostrando todas as subcategorias, que são filhas de supercat (supercategorias) pai;
@login_required
def categoriasView(request,superCat):
    ##verificação de segurança:
    request.session['super_cat'] = superCat
    restaurante_cookie = request.session['restaurante']
    try:
        ##mecanismo de segurança foi implementado
        ## verificando se usuário é proprietario
        restaurante = get_object_or_404(Restaurante,proprietario=request.user,id=restaurante_cookie)
    except:
        ##verificando se usuário é usuário criador
        restaurante = get_object_or_404(Restaurante,usuario_criador=request.user,id=restaurante_cookie)
    superClassificacao = get_object_or_404(Classificacoes, nome_classificacao=superCat,restaurante=restaurante)
    categoria = Item_classificacao.objects.filter(classificacao=superClassificacao)
    quantidade = 0
    for i in categoria:
        quantidade += 1
    context = {
        'categorias' : categoria,'quantidade': quantidade,
    }

    return render(request,'menu/classificacao/subcategoria.html',context=context)

###Adicionando sub-categoria
@login_required
def addCategoria(request):
    if request.method == "GET":
        ##passando restaurante como argumento para o form do init
        ##implementando outro mecanismo de segurança contre fraude nos cookies
        form = FormClassificacao(restaurante=request.session['restaurante'])
        context = {
                'form': form,
        }
        return render (request,'menu/classificacao/add_classificacao.html',context=context)
        
    else:
        
        form = FormClassificacao(request.session['restaurante'],request.POST)
        if form.is_valid():
            form.save()
            return redirect('/meus_produtos/')
                
        else:
            context = {'form': form,}
            return render(request,'menu/classificacao/add_classificacao.html',context=context)
    
### Adicionando super-categoria
@login_required
def addSuperCategoria(request):
    restaurante_cookie = request.session['restaurante']
    ##  mecanismo de segurança sendo implementado abaixo:
    try:
        ## verificando se usuário é proprietário do restaurante
        restaurante = get_object_or_404(Restaurante,id=restaurante_cookie,proprietario=request.user)
    except:
        ## verificando se usuário é usuário criador do restaurante
        restaurante = get_object_or_404(Restaurante,id=restaurante_cookie,usuario_criador=request.user)
    
    ## metodos
    if request.method == "GET":
        form = FormClassificacoes()
        context = {
            'form': form,
                
        }
        return render (request,'menu/classificacao/add_superclassificacao.html',context=context)
        
    else:
        form = FormClassificacoes(request.POST,request.FILES)
        if form.is_valid():
            classificacao = form.cleaned_data['nome_classificacao']
            restaurante_id = request.session['restaurante']
            restaurante = get_object_or_404(Restaurante, id=restaurante_id)
            ##verificando pré-existência
            try:
                get_list_or_404(Classificacoes,restaurante=restaurante,nome_classificacao=classificacao)
                context = {'form': form,}
                return render(request,'menu/classificacao/add_classificacoes.html',context=context)
            except:
                Classificacoes.objects.create(nome_classificacao=classificacao,restaurante=restaurante)
                return redirect ('/meus_produtos/')
        else:
            context = {'form': form,}
            return render(request,'menu/classificacao/add_classificacoes.html',context=context)

### Deletar sub-categoria
@login_required
def deleteCategoria(request,categoria):
    ## verificando se usuario possui categoria para deletar

    ## implementando mecanismo de segurança:
    try:
        restaurante = get_object_or_404(Restaurante,id=request.session['restaurante'],proprietario=request.user)
    except:
        restaurante = get_object_or_404(Restaurante,id=request.session['restaurante'],usuario_criador=request.user)
    ## mesmo não sendo utilizado nesse caso, caso o cookie restaurante não esteja funcionando, o usuário
    ## será redirecionado para a '/escolher_restaurante/'
    try:
        categorias = get_object_or_404(Item_classificacao, text=categoria).delete()
        return redirect ('/meus_produtos/')
    except:
        messages.info(request, 'Seu usuário não possui acesso a edição de dados!')
        return redirect ('/')

### Deletar-remover super-categoria
@login_required
def deleteSuperCategoria(request,super_categoria):
    ## implementando mecanismo de segurança
    try:
        ## verificando se usuário é proprietário do restaurante
        restaurante  = get_object_or_404(Restaurante,id=request.session['restaurante'],proprietario=request.user)
    except:
        ## verificando se usuário é usuário criador do restaurante
        restaurante = get_object_or_404(Restaurante,usuario_criador=request.user,id=request.session['restaurante'])
    try:
        categorias = get_object_or_404(Classificacoes, nome_classificacao=super_categoria,restaurante=restaurante).delete()
        return redirect ('/meus_produtos/')
    except:
        messages.info(request, 'Erro')
        return redirect ('/')

##Editar/atualizar subcategoria, passando novos valores(x=y) sobre os antigos
@login_required
def updateCategoria(request,categoria):
    if request.session['restaurante']:
        post = get_object_or_404(Item_classificacao, text=categoria)
        form = FormClassificacao(restaurante=request.session['restaurante'],instance=post)
        if(request.method == 'POST'):
            form = FormClassificacao(request.session['restaurante'],request.POST,request.FILES, instance=post)
            if(form.is_valid()):
                    post = form.save(commit=False)
                    post.text = form.cleaned_data['text']
                    post.classificacao = form.cleaned_data['classificacao']
                    post.save()
                    return redirect('/meus_produtos/')
    else:
        messages.info(request, 'Erro')
        return redirect ('/')
            
            
       
    context = {'form': form,'post':post,}
    return render(request,'menu/classificacao/edit_categoria.html',context=context)
    
##Atualizar/editar supercategoria, passando novos valores (x=y)
@login_required
def updateSuperCategoria(request,super_categoria):
    restaurante_pk = request.session['restaurante']
    ##implementando mecanismo de segurança
    try:
        ## verificando se usuário é proprietário
        restaurante = get_object_or_404(Restaurante,id=restaurante_pk,proprietario=request.user)
    except:
        ## verificando se usuário é usuário criador
        restaurante = get_object_or_404(Restaurante,id=restaurante_pk,usuario_criador=request.user)
    try:
        post = get_object_or_404(Classificacoes, nome_classificacao=super_categoria,restaurante=restaurante)
        form = FormClassificacoes(instance=post)
        if(request.method == 'POST'):
            form = FormClassificacoes(request.POST,request.FILES, instance=post)
            if(form.is_valid()):
                    post = form.save(commit=False)
                    ##verificando condição de pre-existência
                    try:
                        new_obj_test = get_object_or_404(Classificacoes,nome_classificacao=form.cleaned_data['nome_classificacao'],restaurante=restaurante)
                        if new_obj_test == post:
                            post.nome_classificacao = form.cleaned_data['nome_classificacao']
                            post.save()
                            return redirect('/meus_produtos/')
                           
                        else:
                            ##Em caso de dois cliques, será redirecionado(a) ao menu por motivo de segurança
                             messages.info(request, 'A classificação informada já existe, digite outra classificação e tente novamente!')
                             context = {'form': form,'post':post,}
                             
                             
                    except:
                        post.nome_classificacao = form.cleaned_data['nome_classificacao']
                        post.save()
                        return redirect('/meus_produtos/')        
       
        context = {'form': form,'post':post,}
        return render(request,'menu/classificacao/edit_super_categoria.html',context=context)

    except:
        ##exibir tela de erro 404 ---> Error bad request(404)
        pass

##Filtra por categoria, a super-categoria é passada através do cookie super-categoria
##dado por: request.session['super-cat']
@login_required
def filtrarPorCategoria(request,categoria):
    ##passando o restaurante como parâmetro para achar a respectiva categoria
    try:
        restaurante = get_object_or_404(Restaurante,id=request.session['restaurante'])
    except:
        restaurante = get_object_or_404(Restaurante,usuario_criador=request.user)
    categoria_obj = get_object_or_404(Classificacoes,nome_classificacao=request.session['super_cat'],restaurante=restaurante)
    categoria_var = get_object_or_404(Item_classificacao,text=categoria,classificacao=categoria_obj)
    request.session['classificacao'] = categoria_var.id
    produtos = Item.objects.filter(classificacao = categoria_var)
    quantidade = 0
    for i in produtos:
        quantidade += 1
    
    context = {
        'produtos': produtos,'quantidade':quantidade,
    }
    return render(request,'menu/produtos/produtos_por_categoria.html',context=context)

### Adicionar produto
##MEU PONTO DE PARADA
##COLOCAR PONTO FIXO
@login_required
def adicionarProduto(request):
    print("variável categoria: ")
    print(request.session['classificacao'])
    if request.session['restaurante']:
        if request.method == 'GET':
            ##passar classificação nos forms
            form = FormItens(classificacao=request.session['classificacao'])
            context = {
                'form': form,
            }
            return render(request,'menu/produtos/adicionar_produto.html',context=context)
        else:
            form = FormItens(request.session['classificacao'],request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect ('/meus_produtos/')
            else: 
                context = {'form':form,}
                return render(request,'menu/produtos/adicionar_produto.html',context=context)
    else:
        return redirect('/meus_produtos/')

### editar produto
@login_required
def editarProduto(request,produto):
    if request.session['restaurante']:
        post = get_object_or_404(Item,item_nome=produto)
        form = FormEditItens(instance=post)
        if(request.method == 'POST'):
            form = FormEditItens(request.POST,request.FILES, instance=post)
            if(form.is_valid()):
                    post = form.save(commit=False)
                    post.item_nome = form.cleaned_data['item_nome']
                    post.classificacao = form.cleaned_data['classificacao']
                    post.preco = form.cleaned_data['preco']
                    post.img = form.cleaned_data['img']
                    post.save()
                    return redirect('/meus_produtos/')
                
    
        
        context = {'form': form,'post':post,}
        return render(request,'menu/produtos/editar_produto.html',context=context)
    else:
        return redirect ('/meus_produtos/')
        
###Apagar produto
@login_required
def apagarProduto(request,produto):
    if request.session['restaurante']:
        produto = get_object_or_404(Item,item_nome = produto).delete()
        return redirect ('/meus_produtos/')
    else:
        messages.info(request, 'Seu usuário não possui acesso a edição de dados!')
        return redirect ('/')

###Tela de ajustes
@login_required
def settings(request):
    return render(request,'configuracoes_internas/settings.html')

##tela de boas vindas para novos usuários do virtual_menu
def boas_vindas(request):
    ##tela de bem vindo e cadastre-se para ser usuário do virtual menu
    return redirect('/cardapio/')

