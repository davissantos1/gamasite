from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('', admin.site.urls),  # Painel administrativo
    path('login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='admin-login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/admin/login/'), name='admin-logout'),
]
