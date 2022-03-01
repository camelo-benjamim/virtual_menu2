"""virtual_menu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve 

##
urlpatterns = [
    ##ADMIN AREA
   
    path('admin/', admin.site.urls),
    ###
    path('', include('menu.urls')),
    path('auth/',include('accounts.urls')),
    path('mesa/',include ('mesa.urls')),
    path('pagamento/',include('pagamento.urls')),
    path('cardapio/',include('carrinho.urls')),
    path('relatorios/',include('relatorios.urls')),
    path('push/',include('push.urls')),
    
    ##ADICIONAR MAIN VIEW
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)