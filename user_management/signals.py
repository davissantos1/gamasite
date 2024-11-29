# user_management/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Cria o perfil se não existir
        Profile.objects.get_or_create(user=instance)
    else:
        # Se o perfil já existir, não faz nada
        try:
            instance.profile.save()
        except instance.profile.DoesNotExist:
            Profile.objects.create(user=instance)
