from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import CustomSignupForm
from django.contrib.auth import login

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
