from django.db import models

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
        max_length=50,
        choices=CATEGORY_CHOICES,
        unique=True,
        verbose_name="Categoria"
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria de Leilão"
        verbose_name_plural = "Categorias de Leilão"
