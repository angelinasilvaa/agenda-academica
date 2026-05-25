from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
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
            
            link = f"http://localhost:8000/accounts/ativar/{uid}/{token}/"
            
            send_mail(
                'Ative a sua conta - Agenda Académica',
                f'Clique no link para validar o seu e-mail: {link}',
                'web2@ifce.edu.br',
                [user.email]
            )
            return render(request, 'accounts/cadastro_sucesso.html')
    else:
        form = CadastroForm()
    return render(request, 'accounts/cadastrar.html', {'form': form})

def ativar_conta(request, uidb64, token):
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
        perfil = Perfil.objects.create(user=request.user, email_confirmado=True)

    if not perfil.email_confirmado:
        return render(request, 'accounts/aguardando_confirmacao.html')
        
    meus_compromissos = Compromisso.objects.filter(usuario=request.user)
    
    return render(request, 'accounts/home.html', {
        'compromissos': meus_compromissos,
        'perfil': perfil
    })