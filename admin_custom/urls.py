from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import admin_dashboard

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='admin/login.html', next_page='/admin/dashboard'), name='admin-login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/admin/login/'), name='admin-logout'),
    path('dashboard/', admin_dashboard, name='admin-dashboard'),  # Dashboard personalizado como página inicial
    path('', admin.site.urls),  # URLs padrão do admin
]
