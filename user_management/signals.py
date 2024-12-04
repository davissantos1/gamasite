# user_management/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Arrematante

@receiver(post_save, sender=User)
def create_or_update_user_arrematante(sender, instance, created, **kwargs):
    if created:
        # Cria o perfil se não existir
        Arrematante.objects.get_or_create(user=instance)
    else:
        # Se o perfil já existir, atualiza o perfil
        try:
            instance.arrematante.save()
        except Arrematante.DoesNotExist:
            Arrematante.objects.create(user=instance)
