from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Bid(models.Model):
    """
    Modelo representando os lances feitos no sistema de leilão.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bids",
        verbose_name="Usuário Arrematante"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor do Lance"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data e Hora do Lance"
    )
    is_valid = models.BooleanField(
        default=True,
        verbose_name="Lance Válido"
    )

    class Meta:
        verbose_name = "Lance"
        verbose_name_plural = "Lances"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Lance de {self.user} no item {self.item} - R$ {self.amount:.2f}"

    def get_item_instance(self):
        """
        Retorna a instância concreta do item associado usando GenericForeignKey.
        """
        return self.item



class Payment(models.Model):
    """
    Modelo representando os pagamentos realizados ou pendentes.
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pagamentos",
        verbose_name="Cliente Arrematante"
    )
    # Relacionamento genérico com o modelo de item
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='pagamentos',
        verbose_name='Tipo de Item'
    )
    object_id = models.PositiveIntegerField(verbose_name='ID do Item')
    item = GenericForeignKey('content_type', 'object_id')

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor do Pagamento"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name="Status do Pagamento"
    )
    payment_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data do Pagamento"
    )
    due_date = models.DateField(
        verbose_name="Data de Vencimento"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ["-due_date"]

    def __str__(self):
        return f"Pagamento de {self.user} - R$ {self.amount:.2f} - Status: {self.get_status_display()}"

    @property
    def get_item_instance(self):
        """
        Retorna a instância concreta do item associado usando GenericForeignKey.
        """
        return self.item
