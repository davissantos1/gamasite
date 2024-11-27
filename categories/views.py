# categories/views.py
from django.shortcuts import render

def imoveis(request):
    return render(request, 'categories/imoveis.html')

def veiculos(request):
    return render(request, 'categories/veiculos.html')

def rural(request):
    return render(request, 'categories/rural.html')

def outros_bens(request):
    return render(request, 'categories/outros_bens.html')
