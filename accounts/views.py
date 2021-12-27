from django.core.checks import messages
from django.shortcuts import get_object_or_404, render,redirect
from accounts.forms import UserCreationForm, UserChangeForm, UserDeleteForm
from accounts.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def SignUp(request):
    if request.method == "GET":
        form = UserCreationForm()
        context = {
            'form': form
        }
        return render(request,"user/adduser.html", context=context)
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/meus_produtos/")
            ##REDIRECIONAR PARA DASHBOARD
        
        context = {
                "form": form,
                
            }
    return render(request,"user/adduser.html", context=context)


def Login(request):
    return render(request,"login.html")
@login_required
def ChangeUsr(request):
        usr = request.user
        id_usr = usr.id
    ##O USUÁRIO SÓ PODE DELETAR A SÍ MESMO
    
        post = get_object_or_404(User, pk=id_usr)
        comparation_obj = get_object_or_404(User, pk=id_usr)
        form = UserChangeForm(instance=post)
        if(request.method == 'POST'):
            form = UserChangeForm(request.POST,request.FILES,instance=post)

            if(form.is_valid()):
                post = form.save(commit=False)
                post.companysname = form.cleaned_data['companysname']
                post.main = form.cleaned_data['main']
                post.postal_code = form.cleaned_data['postal_code']
                post.city = form.cleaned_data['city']
                post.state = form.cleaned_data['state']
                post.address = form.cleaned_data['address']
                post.district = form.cleaned_data['district']
                post.number_ref = form.cleaned_data['number_ref']
                post.contacts_phone = form.cleaned_data['contacts_phone']
                
                ##PASSED
                if post.main == False:
                    post.save()
                    return redirect("/settings/")
                ###PASSED
                elif post.main == True and comparation_obj.main == True:
                    post.save
                    return redirect("/settings/")
                else:
                    for i in User.objects.all():
                        if i.main == True:
                            messages.info(request, 'Você já possui uma sede, caso deseje alterar, faça login com a sede atual e desmarque sede nas configurações')
                            return render (request,'user/edit_user.html',{'form':form,'post':post,})
                    post.save()
                ##REVERSE NOT FOUND
            
        
        return render(request, 'user/edit_user.html', {'form': form, 'post' : post})

@login_required
def usrDelete(request):

    if request.method == "GET":
        current_user = request.user
        id_usr = current_user.username
        form = UserDeleteForm()

        context = {
            'form': form,
            'id_usr': id_usr,
        }
    else:
        try: 
            form = UserDeleteForm(request.POST)
            ## if user = request.user
            user = form['username'].value()
            u = User.objects.get(username=user)
            u.delete()
            return redirect ('/auth/user_deleted/')

        except User.DoesNotExist:   
            return render(request, 'user/delete_error.html')

        except Exception as e: 
            return render(request, 'user/delete_error.html')

        
    return render(request, 'user/delete_user.html',context)

def userDeleted(request):
    return render(request, "user/user_deleted.html")