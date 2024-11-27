# auction_management/views.py
from django.shortcuts import render

def leiloes_ao_vivo(request):
    return render(request, 'auction_management/leiloes_ao_vivo.html')

def calendario(request):
    return render(request, 'auction_management/calendario.html')