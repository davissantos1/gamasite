# categories/views.py
from django.shortcuts import render
from auction_management.models import Vehicle, RealEstate, RuralItem, OtherGoods  

def imoveis(request):
    imoveis = RealEstate.objects.all()  
    return render(request, 'categories/imoveis.html', {'imoveis': imoveis})

def veiculos(request):
    veiculos = Vehicle.objects.all()  
    return render(request, 'categories/veiculos.html', {'veiculos': veiculos})

def rural(request):
    rural = RuralItem.objects.all()  
    return render(request, 'categories/rural.html', {'rural': rural})

def outros_bens(request):
    outros_bens = OtherGoods.objects.all()  
    return render(request, 'categories/outros_bens.html', {'outros_bens': outros_bens})
