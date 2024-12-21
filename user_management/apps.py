# user_management/apps.py
from django.apps import AppConfig

class UserManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_management'

    def ready(self):
        """
        Método chamado quando a aplicação é carregada. Importa os sinais para garantir que eles sejam registrados.
        """
        from . import signals  # Importação explícita para registrar os sinais
