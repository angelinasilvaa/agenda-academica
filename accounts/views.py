from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

from .forms import CadastroForm
from .models import Perfil
from agenda.models import Compromisso 

def cadastrar(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save() 
            
            Perfil.objects.create(user=user, foto=form.cleaned_data['foto'])
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            link_ativacao = request.build_absolute_uri(
                f"/accounts/ativar/{uid}/{token}/"
            )
            
            send_mail(
                'Ative a sua conta - Agenda Académica',
                f'Clique no link para validar o seu e-mail: {link_ativacao}',
                'webmaster@localhost',
                [user.email]
            )
            return render(request, 'accounts/aguardando_confirmacao.html', {
                'link_ativacao': link_ativacao
            })
    else:
        form = CadastroForm()
    return render(request, 'accounts/cadastrar.html', {'form': form})

def activar_conta(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        perfil = user.perfil
        perfil.email_confirmado = True
        perfil.save()
        return redirect('login')
    else:
        return render(request, 'accounts/token_invalido.html')

@login_required
def home(request):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        perfil = Perfil.objects.create(user=request.user)
        
    if not perfil.email_confirmado:
        return render(request, 'accounts/aguardando_confirmacao.html')
        
    # CORREÇÃO: Ordenado pelo campo real 'data_hora'
    meus_compromissos = Compromisso.objects.filter(usuario=request.user).order_by('data_hora')
    
    # Lógica do Alerta (Avisar 3 dias antes)
    hoje = timezone.now().date()
    tres_dias_depois = hoje + timedelta(days=3)
    
    alertas = []
    for comp in meus_compromissos:
        if comp.data_hora:
            # Extrai apenas a data se for um objeto datetime
            data_compromisso = comp.data_hora.date() if hasattr(comp.data_hora, 'date') else comp.data_hora
            if not comp.concluido and hoje <= data_compromisso <= tres_dias_depois:
                alertas.append(comp)
    
    return render(request, 'accounts/home.html', {
        'compromissos': meus_compromissos,
        'perfil': perfil,
        'alertas': alertas,
    })

# --- CONTROLES DE COMPROMISSO DIRETOS DO UTILIZADOR ---

@login_required
def adicionar_compromisso(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data_hora = request.POST.get('data_hora')
        tipo = request.POST.get('tipo', 'OUTRO')
        
        if titulo and data_hora:
            Compromisso.objects.create(
                usuario=request.user,
                titulo=titulo,
                descricao=descricao,
                data_hora=data_hora,
                tipo=tipo
            )
    return redirect('home')

@login_required
def concluir_compromisso(request, pk):
    compromisso = get_object_or_404(Compromisso, pk=pk, usuario=request.user)
    compromisso.concluido = True
    compromisso.save()
    return redirect('home')

@login_required
def eliminar_compromisso(request, pk):
    compromisso = get_object_or_404(Compromisso, pk=pk, usuario=request.user)
    compromisso.delete()
    return redirect('home')
def inicial(request):
    return render(request, 'accounts/inicial.html')