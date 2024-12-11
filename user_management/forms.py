import re
import requests
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Arrematante, Documento

class CustomSignupForm(UserCreationForm):
    TIPO_CADASTRO_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    ]

    username = forms.CharField(max_length=150, label='Nome de Usuário')
    first_name = forms.CharField(max_length=30, label='Nome')
    last_name = forms.CharField(max_length=30, label='Sobrenome')
    email = forms.EmailField(max_length=254, label='E-mail')
    cpf_cnpj = forms.CharField(max_length=30, label='CPF/CNPJ')
    cep = forms.CharField(max_length=9, label='CEP')
    logradouro = forms.CharField(max_length=255, label='Logradouro')
    numero = forms.CharField(max_length=10, label='Número')
    complemento = forms.CharField(max_length=255, required=False, label='Complemento')
    bairro = forms.CharField(max_length=100, label='Bairro')
    cidade = forms.CharField(max_length=100, label='Cidade')
    estado = forms.CharField(max_length=50, label='Estado')
    pais = forms.ChoiceField(choices=[('Brasil', 'Brasil')], initial='Brasil', label='País')
    telefone_comercial = forms.CharField(max_length=15, required=False, label='Telefone Comercial')
    telefone_celular = forms.CharField(max_length=15, label='Telefone Celular')
    tipo_cadastro = forms.ChoiceField(
        choices=TIPO_CADASTRO_CHOICES,
        widget=forms.RadioSelect,
        label='Tipo de Cadastro'
    )

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2',
        )

    def clean_cpf_cnpj(self):
        cpf_cnpj = self.cleaned_data['cpf_cnpj'].strip().replace('.', '').replace('/', '').replace('-', '')  # Remove os caracteres especiais
        
        cpf_pattern = r'^\d{11}$'  # Apenas números, 11 dígitos para CPF
        cnpj_pattern = r'^\d{14}$'  # Apenas números, 14 dígitos para CNPJ

        if not re.match(cpf_pattern, cpf_cnpj) and not re.match(cnpj_pattern, cpf_cnpj):
            raise ValidationError("CPF ou CNPJ inválido. Use os formatos: 000.000.000-00 para CPF e 00.000.000/0000-00 para CNPJ.")
        
        return self.cleaned_data['cpf_cnpj']

    def clean(self):
        cleaned_data = super().clean()
        cpf_cnpj = cleaned_data.get('cpf_cnpj')
        tipo_cadastro = cleaned_data.get('tipo_cadastro')

        cpf_pattern = r'^\d{11}$'
        cnpj_pattern = r'^\d{14}$'

        if tipo_cadastro == 'PF' and not re.match(cpf_pattern, cpf_cnpj.replace('.', '').replace('-', '').replace('/', '')):
            raise ValidationError("Para Pessoas Físicas, insira um CPF válido.")
        if tipo_cadastro == 'PJ' and not re.match(cnpj_pattern, cpf_cnpj.replace('.', '').replace('-', '').replace('/', '')):
            raise ValidationError("Para Pessoas Jurídicas, insira um CNPJ válido.")
        
        return cleaned_data


    def clean_cep(self):
        cep = self.cleaned_data['cep'].strip()
        if not re.match(r'^\d{5}-\d{3}$', cep):
            raise ValidationError("CEP inválido. Use o formato 00000-000.")

        # Consulta API ViaCEP para preencher o endereço automaticamente
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        if response.status_code == 200:
            data = response.json()
            if 'erro' in data:
                raise ValidationError("CEP não encontrado.")
            self.cleaned_data['logradouro'] = data.get('logradouro', '')
            self.cleaned_data['bairro'] = data.get('bairro', '')
            self.cleaned_data['cidade'] = data.get('localidade', '')
            self.cleaned_data['estado'] = data.get('uf', '')
        else:
            raise ValidationError("Não foi possível validar o CEP.")
        return cep

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        # Verificar se o Arrematante já existe para este usuário
        arrematante, created = Arrematante.objects.get_or_create(
            user=user,
            defaults={
                'cpf_cnpj': self.cleaned_data['cpf_cnpj'],
                'cep': self.cleaned_data['cep'],
                'logradouro': self.cleaned_data['logradouro'],
                'numero': self.cleaned_data['numero'],
                'complemento': self.cleaned_data['complemento'],
                'bairro': self.cleaned_data['bairro'],
                'cidade': self.cleaned_data['cidade'],
                'estado': self.cleaned_data['estado'],
                'pais': self.cleaned_data['pais'],
                'telefone_comercial': self.cleaned_data['telefone_comercial'],
                'telefone_celular': self.cleaned_data['telefone_celular'],
                'tipo_cadastro': self.cleaned_data['tipo_cadastro'],
            }
        )

        # Se o Arrematante já existe, atualize os campos
        if not created:
            arrematante.cpf_cnpj = self.cleaned_data['cpf_cnpj']
            arrematante.cep = self.cleaned_data['cep']
            arrematante.logradouro = self.cleaned_data['logradouro']
            arrematante.numero = self.cleaned_data['numero']
            arrematante.complemento = self.cleaned_data['complemento']
            arrematante.bairro = self.cleaned_data['bairro']
            arrematante.cidade = self.cleaned_data['cidade']
            arrematante.estado = self.cleaned_data['estado']
            arrematante.pais = self.cleaned_data['pais']
            arrematante.telefone_comercial = self.cleaned_data['telefone_comercial']
            arrematante.telefone_celular = self.cleaned_data['telefone_celular']
            arrematante.tipo_cadastro = self.cleaned_data['tipo_cadastro']
            arrematante.save()

        return user

class ArrematanteEditForm(forms.ModelForm):
    class Meta:
        model = Arrematante
        fields = [
            'tipo_cadastro',  
            'cpf_cnpj',
            'cep',
            'logradouro',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'estado',
            'pais',
            'telefone_comercial',
            'telefone_celular',
        ]

    tipo_cadastro = forms.ChoiceField(
        choices=Arrematante.TIPO_CADASTRO_CHOICES,
        widget=forms.RadioSelect,  
        label="Tipo de Cadastro",
    )


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['tipo_documento', 'documento']
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'documento': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
