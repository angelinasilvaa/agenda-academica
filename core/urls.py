"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include  # <-- O 'include' é obrigatório aqui para importar as rotas das outras pastas!
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Rota de administração nativa
    path('admin/', admin.site.urls),
    
    # 2. Rotas nativas de autenticação do Django (login, logout, reset de senha)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # 3. Rotas da nova aplicação de usuários (cadastro, confirmação)
    path('accounts/', include('accounts.urls')),
    
    # 4. Rota principal do seu app de Agenda antiga
    path('', include('agenda.urls')),
]

# Libera a visualização das fotos de perfil carregadas pelo usuário no navegador
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
