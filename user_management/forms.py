# user_management/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='Nome')
    last_name = forms.CharField(max_length=30, label='Sobrenome')
    email = forms.EmailField(max_length=254, label='E-mail', help_text='Um endereço de e-mail válido.')
    cpf_cnpj = forms.CharField(max_length=18, label='CPF/CNPJ')
    cep = forms.CharField(max_length=9, label='CEP')
    logradouro = forms.CharField(max_length=255, label='Logradouro')
    numero = forms.CharField(max_length=10, label='Número')
    complemento = forms.CharField(max_length=255, required=False, label='Complemento')
    bairro = forms.CharField(max_length=100, label='Bairro')
    cidade = forms.CharField(max_length=100, label='Cidade')
    estado = forms.CharField(max_length=50, label='Estado')
    pais = forms.ChoiceField(choices=[
        ('Brasil', 'Brasil'),
        ('Argentina', 'Argentina'),
        ('Chile', 'Chile'),
        # Adicione outros países conforme necessário
    ], initial='Brasil', label='País')
    telefone_comercial = forms.CharField(max_length=15, required=False, label='Telefone Comercial')
    telefone_celular = forms.CharField(max_length=15, label='Telefone Celular')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = Profile(user=user)
            profile.cpf_cnpj = self.cleaned_data['cpf_cnpj']
            profile.cep = self.cleaned_data['cep']
            profile.logradouro = self.cleaned_data['logradouro']
            profile.numero = self.cleaned_data['numero']
            profile.complemento = self.cleaned_data['complemento']
            profile.bairro = self.cleaned_data['bairro']
            profile.cidade = self.cleaned_data['cidade']
            profile.estado = self.cleaned_data['estado']
            profile.pais = self.cleaned_data['pais']
            profile.telefone_comercial = self.cleaned_data['telefone_comercial']
            profile.telefone_celular = self.cleaned_data['telefone_celular']
            profile.save()
        return user

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        
        profile = Profile(user=user)
        profile.cpf_cnpj = self.cleaned_data['cpf_cnpj']
        profile.cep = self.cleaned_data['cep']
        profile.logradouro = self.cleaned_data['logradouro']
        profile.numero = self.cleaned_data['numero']
        profile.complemento = self.cleaned_data['complemento']
        profile.bairro = self.cleaned_data['bairro']
        profile.cidade = self.cleaned_data['cidade']
        profile.estado = self.cleaned_data['estado']
        profile.pais = self.cleaned_data['pais']
        profile.telefone_comercial = self.cleaned_data['telefone_comercial']
        profile.telefone_celular = self.cleaned_data['telefone_celular']
        profile.save()
        return user
