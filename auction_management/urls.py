# auction_management/urls.py
from django.urls import path
from . import views

app_name = 'auction_management'

urlpatterns = [
    path('leiloes_ao_vivo/', views.leiloes_ao_vivo, name='leiloes_ao_vivo'),
    path('calendario/', views.calendario, name='calendario'),
]
