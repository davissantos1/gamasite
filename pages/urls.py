# pages/urls.py
from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='home'),
    path('como-participar/', views.como_participar, name='como_participar'),
    path('leiloes_ao_vivo/', views.leiloes_ao_vivo, name='leiloes_ao_vivo'),
    path('calendario/', views.calendario, name='calendario'),
    path('item/<int:id>/', views.item_detail, name='item_detail'),
    path('leilao/<str:id>/', views.leilao_detalhe, name='leilao_detalhe'),
    path('dashboard/inicio/', views.inicio, name='inicio'),
    path('dashboard/lotes/', views.lotes, name='lotes'),
    path('dashboard/lances/', views.lances, name='lances'),
    path('financeiro/', views.financeiro_cliente, name='financeiro_cliente'),
]
