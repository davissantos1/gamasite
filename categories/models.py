from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class AuctionCategory(models.Model):
    # Definindo as opções de categorias
    IMOVEIS = 'Imóveis'
    VEICULOS = 'Veículos'
    RURAL = 'Rural'
    OUTROS_BENS = 'Outros Bens'

    CATEGORY_CHOICES = [
        (IMOVEIS, 'Imóveis'),
        (VEICULOS, 'Veículos'),
        (RURAL, 'Rural'),
        (OUTROS_BENS, 'Outros Bens'),
    ]

    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nome da Categoria",
        choices=CATEGORY_CHOICES
    )
    descricao = models.TextField(verbose_name="Descrição", blank=True, null=True)

    # Relacionamento genérico para o featured_item
    # Usamos ContentType para permitir que o featured_item possa ser de qualquer tipo de item
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='featured_items'
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    featured_item = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria de Leilão"
        verbose_name_plural = "Categorias de Leilão"
