from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomSignupForm, ProfileEditForm, UserEditForm
from allauth.account.forms import LoginForm
from django.contrib.auth.decorators import login_required

def custom_login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        form.login(request)
        return redirect('home')  # ou onde deseja redirecionar após o login bem-sucedido
    return render(request, 'account/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Opcional: faz login automático após cadastro
            return redirect('home')  # Redireciona para a página inicial, por exemplo
        else:
            # Se o formulário não for válido, ele retornará à página com erros
            return render(request, 'signup.html', {'form': form})
    else:
        form = CustomSignupForm()
    return render(request, 'signup.html', {'form': form})


def profile_view(request):
    # Adicione qualquer lógica necessária para exibir o perfil
    return render(request, 'accounts/profile.html')


@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def profile_details(request):
    return render(request, 'accounts/profile_details.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, instance=request.user.profile)
        user_form = UserEditForm(request.POST, instance=request.user)
        
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('account_profile')
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
        user_form = UserEditForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {
        'profile_form': profile_form,
        'user_form': user_form,
    })

