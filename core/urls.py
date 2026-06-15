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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views  # IMPORTANTE: Adicione essa linha para o arquivo conhecer o 'views'

urlpatterns = [
    # 1. Rota de administração nativa
    path('admin/', admin.site.urls),

    # 2. Rotas nativas de autenticação do Django
    path('accounts/', include('django.contrib.auth.urls')),

    # 3. Rotas da nova aplicação de usuários
    path('accounts/', include('accounts.urls')),

    # 4. ROTA INICIAL DO APLICATIVO (Modificada aqui!)
    path('', views.inicial, name='inicial'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
