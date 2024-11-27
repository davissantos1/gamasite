# categories/urls.py
from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('imoveis/', views.imoveis, name='imoveis'),
    path('veiculos/', views.veiculos, name='veiculos'),
    path('rural/', views.rural, name='rural'),
    path('outros_bens/', views.outros_bens, name='outros_bens'),
]
