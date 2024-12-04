from django.db import models
from auction_management.models import BaseItem

class AuctionCategory(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Nome da Categoria")
    descricao = models.TextField(verbose_name="Descrição", null=True, blank=True)  # Campo de descrição
    featured_item = models.ForeignKey(
        BaseItem,
        on_delete=models.SET_NULL,
        null=True,
        related_name="featured_in_category"
    )

    def __str__(self):
        return self.nome
