# pages/views.py

from django.shortcuts import render

def index(request):
    return render(request, 'pages/index.html')

def como_participar(request):
    return render(request, 'pages/como_participar.html')


