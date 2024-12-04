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
]
