from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='account_profile'),
    path('profile/details/', views.profile_details, name='account_profile_details'),
    path('profile/edit/', views.edit_profile, name='account_edit_profile'),
    path('profile/leiloes/', views.leiloes_view, name='account_leilao'),  # Página de Leilões
    path('profile/lances/', views.lances_view, name='account_lance'),  # Página de Lances
    path('profile/financeiro/', views.financeiro_view, name='account_financeiro'),  # Página Financeiro
    path('profile/documentos/', views.documentos_view, name='account_documentos'),  # Página Documentos
    path('documentos/<int:documento_id>/', views.serve_documento, name='serve_documento'),
    path('', include('allauth.urls')),
]

