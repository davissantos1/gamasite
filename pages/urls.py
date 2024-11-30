# pages/urls.py
from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='home'),
    path('como-participar/', views.como_participar, name='como_participar'),
]
