from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('ativar/<uidb64>/<token>/', views.activar_conta, name='ativar_conta'),
    path('compromisso/adicionar/', views.adicionar_compromisso, name='adicionar_compromisso'),
    path('compromisso/concluir/<int:pk>/', views.concluir_compromisso, name='concluir_compromisso'),
    path('compromisso/eliminar/<int:pk>/', views.eliminar_compromisso, name='eliminar_compromisso'),
    path('inicial/', views.inicial, name='inicial'),
]