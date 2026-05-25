from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class CadastroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
    foto = forms.ImageField(required=False, label="Foto de Perfil")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
