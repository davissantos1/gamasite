import logging
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from .models import Arrematante, Admin

logger = logging.getLogger(__name__)

class UserTypeAccessControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define o caminho atual da requisição
        current_path = request.path
        logger.debug(f"Request path: {current_path}")  # Log para verificar o caminho da requisição

        # Defina as URLs de acesso no front-end para arrematantes e administradores
        front_end_urls = ('/', 'categories', 'accounts', 'account', '')  # Ajuste com o prefixo das URLs do front-end
        admin_urls = '/admin/'  # Prefixo de URL para painel de administração

        # Inicializa user_type com valor padrão
        user_type = None

        if request.user.is_authenticated:
            # Log para verificar os detalhes do usuário
            logger.debug(f"Authenticated user: {request.user.username}, Superuser: {request.user.is_superuser}, User type: {getattr(request.user, 'user_type', 'None')}")

            # Verifique o tipo de usuário, considerando modelos estendidos
            if hasattr(request.user, 'user_type'):
                user_type = request.user.user_type
            elif isinstance(request.user, Arrematante):
                user_type = 'arrematante'
            elif isinstance(request.user, Admin):
                user_type = 'admin'

            # Para o superusuário que não tem user_type, tratá-lo com um valor padrão
            if user_type is None and request.user.is_superuser:
                user_type = 'superuser'

            logger.debug(f"User type: {user_type}, Request path: {current_path}")

            # Caso o superusuário tente acessar o front-end
            if user_type == 'superuser' and any(current_path.startswith(url) for url in front_end_urls):
                messages.warning(request, "Superusuários não têm acesso ao front-end.")
                logger.debug(f"Superusuário {request.user.username} tentando acessar o front-end. Redirecionando para logout.")
                return redirect(reverse('admin:logout'))  # Redireciona para o logout do admin

            # Caso o usuário seja admin e tente acessar o front-end
            if user_type == 'admin' and any(current_path.startswith(url) for url in front_end_urls):
                messages.warning(request, "Admins não têm acesso ao front-end.")
                logger.debug(f"Admin {request.user.username} tentando acessar o front-end. Redirecionando para logout.")
                return redirect(reverse('admin:logout'))  # Verifique se o nome está correto

            # Caso o usuário seja arrematante e tente acessar o painel de administração
            if user_type == 'arrematante' and current_path.startswith(admin_urls):
                messages.warning(request, "Arrematantes não têm acesso ao painel de administração.")
                logger.debug(f"Arrematante {request.user.username} tentando acessar o painel de administração. Redirecionando para logout.")
                return redirect(reverse('admin_custom:logout'))  # Redirecionamento para a URL do arrematante (confirme o nome exato da URL)

        # No caso de um usuário não autenticado ou outro cenário, loga um user_type padrão
        logger.debug(f"Current path: {current_path}, User type: {user_type}")
        logger.debug("Middleware acionado!")  # Log para verificar se o middleware está sendo chamado

        # Chama a resposta da requisição
        response = self.get_response(request)
        return response
