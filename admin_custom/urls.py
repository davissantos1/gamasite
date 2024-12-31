from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import admin_dashboard, admin_ao_vivo, iniciar_ao_vivo, finalizar_leilao, proximo_item_leilao

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='admin/login.html', next_page='/admin/dashboard'), name='admin-login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/admin/login/'), name='admin-logout'),
    path('dashboard/', admin_dashboard, name='admin-dashboard'),  # Dashboard personalizado como página inicial
    path('ao-vivo/', admin_ao_vivo, name='admin-ao-vivo'),  
    path('iniciar-ao-vivo/<str:codigo_leilao>/', iniciar_ao_vivo, name='iniciar_ao_vivo'),
    path('finalizar-leilao/<str:codigo_leilao>/', finalizar_leilao, name='finalizar_leilao'),
    path('proximo_item_leilao/<str:codigo_leilao>/', proximo_item_leilao, name='proximo_item_leilao'),
    path('', admin.site.urls),  # URLs padrão do admin
]
