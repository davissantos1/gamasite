from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomSignupForm, ArrematanteEditForm, UserEditForm
from allauth.account.forms import LoginForm
from django.contrib.auth.decorators import login_required
from .models import Arrematante

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
            # Retorna o formulário com erros, se houver
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
