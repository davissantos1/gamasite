# user_management/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Arrematante, Admin

@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    """
    Sinal para criar perfis automaticamente após a criação de um usuário e atualizar o campo user_type.
    """
    if created:
        # Cria o perfil de Arrematante como padrão
        if not hasattr(instance, "arrematante"):
            Arrematante.objects.create(
                user=instance,
                cpf_cnpj='',  # Campos padrão
                cep='',
                logradouro='',
                numero='',
                complemento='',
                bairro='',
                cidade='',
                estado='',
                pais='',
                telefone_comercial='',
                telefone_celular='',
                tipo_cadastro='PF',  # Tipo padrão Pessoa Física
            )

        # Cria o perfil de Admin, caso necessário (com base em lógica futura)
        if not hasattr(instance, "admin"):
            Admin.objects.create(
                user=instance,
                setor='',  # Dados padrão
                telefone='',  # Dados padrão
            )

    # Atualiza o campo `user_type` para refletir o perfil criado
    user_type = 'default'  # Valor padrão
    if hasattr(instance, "arrematante"):
        user_type = 'arrematante'
    elif hasattr(instance, "admin"):
        user_type = 'admin'

    # Evita salvar o usuário se o valor de user_type não mudou
    if instance.user_type != user_type:
        instance.user_type = user_type
        instance.save(update_fields=["user_type"])
