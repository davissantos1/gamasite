from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomSignupForm, ArrematanteEditForm, UserEditForm
from allauth.account.forms import LoginForm
from django.contrib.auth.decorators import login_required
from .models import Arrematante, Documento
from .forms import DocumentoForm
from django.conf import settings
from django.http import HttpResponse, Http404
import os

def custom_login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        form.login(request)
        return redirect('home')  # Redireciona após login bem-sucedido
    return render(request, 'account/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Faz login automático após cadastro
            return redirect('home')  # Redireciona para a página inicial
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = CustomSignupForm()
    return render(request, 'signup.html', {'form': form})


def profile_view(request):
    documentos_pendentes = []

    if request.user.is_authenticated:
        arrematante = request.user.arrematante

        if arrematante.tipo_cadastro == 'PF':
            if not arrematante.documentos.filter(tipo_documento='RG').exists():
                if not arrematante.documentos.filter(tipo_documento='CNH').exists():
                    if not arrematante.documentos.filter(tipo_documento='PASSAPORTE').exists():
                        documentos_pendentes.append('Identidade (RG, CNH ou Passaporte)')
                
            if not arrematante.documentos.filter(tipo_documento='COMPROVANTE_RESIDENCIA').exists():
                documentos_pendentes.append('Comprovante de residência')
            if not arrematante.documentos.filter(tipo_documento='SELFIE').exists():
                documentos_pendentes.append('Selfie')

        elif arrematante.tipo_cadastro == 'PJ':
            if not arrematante.documentos.filter(tipo_documento='CONTRATO_SOCIAL').exists():
                documentos_pendentes.append('Contrato Social')
            if not arrematante.documentos.filter(tipo_documento='COMPROVANTE_RESIDENCIA').exists():
                documentos_pendentes.append('Comprovante de residência')
            if not arrematante.documentos.filter(tipo_documento='SELFIE').exists():
                documentos_pendentes.append('Selfie')

    return render(request, 'accounts/profile.html', {
        'documentos_pendentes': documentos_pendentes,
    })


@login_required
def profile_details(request):
    """
    Detalhes do perfil do usuário.
    """
    try:
        arrematante = request.user.arrematante
    except Arrematante.DoesNotExist:
        arrematante = None

    return render(request, 'accounts/profile_details.html', {
        'arrematante': arrematante,
    })


@login_required
def edit_profile(request):
    """
    Permite que o usuário edite seu perfil e suas informações pessoais.
    """
    try:
        arrematante = request.user.arrematante
    except Arrematante.DoesNotExist:
        return redirect('profile')  # Redireciona caso o perfil não exista

    if request.method == 'POST':
        profile_form = ArrematanteEditForm(request.POST, instance=arrematante)
        user_form = UserEditForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('account_profile')
    else:
        profile_form = ArrematanteEditForm(instance=arrematante)
        user_form = UserEditForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {
        'profile_form': profile_form,
        'user_form': user_form,
    })


@login_required
def leiloes_view(request):
    """
    Exibe os leilões do usuário.
    """
    try:
        arrematante = request.user.arrematante  # Obtém o arrematante
        leiloes = arrematante.leiloes.all()  # Supondo que o arrematante tenha uma relação com leilões
    except Arrematante.DoesNotExist:
        leiloes = []  # Caso não haja arrematante, retorna uma lista vazia

    return render(request, 'accounts/leiloes.html', {
        'leiloes': leiloes,
    })


@login_required
def lances_view(request):
    """
    Exibe os lances feitos pelo usuário.
    """
    try:
        arrematante = request.user.arrematante
        lances = arrematante.lances.all()  # Supondo que o arrematante tenha uma relação com lances
    except Arrematante.DoesNotExist:
        lances = []  # Caso não haja arrematante, retorna uma lista vazia

    return render(request, 'accounts/lances.html', {
        'lances': lances,
    })


@login_required
def serve_documento(request, documento_id):
    try:
        documento = Documento.objects.get(id=documento_id)
    except Documento.DoesNotExist:
        raise Http404("Documento não encontrado.")
    
    # Verifique se o usuário autenticado é o usuário associado ao arrematante do documento
    if documento.arrematante.user != request.user:
        raise Http404("Você não tem permissão para acessar este documento.")
    
    # Caminho para o arquivo
    file_path = os.path.join(settings.PROTECTED_DOCUMENTS_DIR, documento.documento.name)
    
    # Verifique se o arquivo realmente existe
    if not os.path.exists(file_path):
        raise Http404("Arquivo não encontrado.")
    
    # Servir o arquivo
    with open(file_path, 'rb') as f:
        return HttpResponse(f.read(), content_type="application/pdf")


@login_required
def documentos_view(request):
    user = request.user
    arrematante = user.arrematante if hasattr(user, 'arrematante') else None
    
    # Defina os tipos de documentos permitidos com base no tipo de arrematante
    if arrematante and arrematante.tipo_cadastro == 'PF':
        tipos_documentos_permitidos = ['RG', 'CNH', 'PASSAPORTE', 'SELFIE', 'COMPROVANTE_RESIDENCIA']
    elif arrematante and arrematante.tipo_cadastro == 'PJ':
        tipos_documentos_permitidos = ['COMPROVANTE_RESIDENCIA', 'CONTRATO_SOCIAL', 'SELFIE']
    else:
        tipos_documentos_permitidos = []

    # Obtenha os documentos do arrematante
    documentos = Documento.objects.filter(arrematante=arrematante)

    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            # Verifica se há documentos anteriores
            documentos_existentes = Documento.objects.filter(arrematante=arrematante, tipo_documento=documento.tipo_documento)
            for doc in documentos_existentes:
                if doc.status == 'P':  # Se houver documento pendente, não permita o envio
                    return render(request, 'accounts/documentos.html', {
                        'form': form,
                        'documentos': documentos,
                        'tipos_documentos_permitidos': tipos_documentos_permitidos,
                        'arrematante': arrematante,
                        'erro': 'Você já possui um documento pendente para esse tipo.',
                    })
            documento.arrematante = arrematante
            documento.save()
            return redirect('account_documentos')  # Redirecionar após o envio do documento
    else:
        form = DocumentoForm()

    return render(request, 'accounts/documentos.html', {
        'documentos': documentos,
        'tipos_documentos_permitidos': tipos_documentos_permitidos,
        'arrematante': arrematante,
        'form': form,
    })


@login_required
def financeiro_view(request):
    """
    Exibe as informações financeiras do usuário.
    """
    try:
        arrematante = request.user.arrematante
        financeiro = arrematante.financeiro  # Supondo que o arrematante tenha uma relação com financeiro
    except Arrematante.DoesNotExist:
        financeiro = None  # Caso não haja arrematante, retorna None

    return render(request, 'accounts/financeiro.html', {
        'financeiro': financeiro,
    })
