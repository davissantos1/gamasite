# user_management/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Arrematante, Admin

# Sinais para criar perfis automaticamente após a criação de um usuário
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Criar perfil de Arrematante
        if hasattr(instance, "arrematante") and not instance.arrematante:
            arrematante = Arrematante.objects.create(
                user=instance,
                cpf_cnpj='',  # Inicializar com dados vazios ou valores padrão
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
                tipo_cadastro='',  # Valor padrão para tipo de cadastro
            )
            arrematante.save()

        # Criar perfil de Admin
        elif hasattr(instance, "admin") and not instance.admin:
            admin = Admin.objects.create(
                user=instance,
                setor='',  # Pode preencher com dados padrão
                telefone='',  # Pode preencher com dados padrão
            )
            admin.save()

    else:
        # Atualizar os dados do Arrematante após o usuário ser salvo
        if hasattr(instance, "arrematante"):
            arrematante = instance.arrematante
            # Verifique se o arrematante possui todos os dados necessários e os atualize
            arrematante.cpf_cnpj = instance.arrematante.cpf_cnpj or arrematante.cpf_cnpj
            arrematante.cep = instance.arrematante.cep or arrematante.cep
            arrematante.logradouro = instance.arrematante.logradouro or arrematante.logradouro
            arrematante.numero = instance.arrematante.numero or arrematante.numero
            arrematante.complemento = instance.arrematante.complemento or arrematante.complemento
            arrematante.bairro = instance.arrematante.bairro or arrematante.bairro
            arrematante.cidade = instance.arrematante.cidade or arrematante.cidade
            arrematante.estado = instance.arrematante.estado or arrematante.estado
            arrematante.pais = instance.arrematante.pais or arrematante.pais
            arrematante.telefone_comercial = instance.arrematante.telefone_comercial or arrematante.telefone_comercial
            arrematante.telefone_celular = instance.arrematante.telefone_celular or arrematante.telefone_celular
            arrematante.tipo_cadastro = instance.arrematante.tipo_cadastro or arrematante.tipo_cadastro

            arrematante.save()

# Sinal para salvar perfil do usuário
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "arrematante"):
        instance.arrematante.save()
    elif hasattr(instance, "admin"):
        instance.admin.save()
