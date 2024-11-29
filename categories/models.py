from django.db import models

class AuctionCategory(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Nome da Categoria")

    def __str__(self):
        return self.nome
