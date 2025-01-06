from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Auction

# Signal para garantir que o status seja atualizado automaticamente antes de salvar
@receiver(pre_save, sender=Auction)
def auto_update_status(sender, instance, **kwargs):
    instance.update_status()