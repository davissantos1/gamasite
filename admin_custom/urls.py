from django.urls import path
from .views import list_clients, admin_dashboard, list_auctions, list_items
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='admin/login.html', next_page='/admin/'), name='admin-login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/admin/login/'), name='admin-logout'),
    path('clients/', list_clients, name='list-clients'),
    path('auctions/', list_auctions, name='list-auctions'),
    path('itens/', list_items, name='list-items'),
    path('', admin_dashboard, name='admin-dashboard'),  # Dashboard personalizado como página inicial
    path('', admin.site.urls),  # URLs padrão do admin
]
