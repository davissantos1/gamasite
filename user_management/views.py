from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomSignupForm, ArrematanteEditForm, UserEditForm
from allauth.account.forms import LoginForm
from django.contrib.auth.decorators import login_required
from .models import Arrematante, Documento
from .forms import DocumentoForm

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


@login_required
def profile_view(request):
    """
    Exibe informações do perfil do usuário logado.
    """
    try:
        arrematante = request.user.arrematante  # Tenta acessar o perfil do arrematante
    except Arrematante.DoesNotExist:
        arrematante = None  # Caso não exista perfil, retorna None

    return render(request, 'accounts/profile.html', {
        'arrematante': arrematante,
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
def documentos_view(request):
    try:
        arrematante = request.user.arrematante
    except Arrematante.DoesNotExist:
        arrematante = None
    
    documentos = arrematante.documentos.all() if arrematante else []

    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            if arrematante:
                documento.arrematante = arrematante
            if request.user.vendedor:
                documento.vendedor = request.user.vendedor
            documento.save()
            return redirect('documentos')  # Redireciona para a página de documentos
    else:
        form = DocumentoForm()

    return render(request, 'accounts/documentos.html', {
        'documentos': documentos,
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
