from django.db import models
from django.conf import settings

class Bid(models.Model):
    """
    Modelo representando os lances feitos no sistema de leilão.
    """
    item = models.ForeignKey(
        'auction_management.RuralItem',  # Substituir por uma subclasse concreta de BaseItem
        on_delete=models.CASCADE,
        related_name='bids',
        verbose_name='Item'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bids",
        verbose_name="Usuário"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor do Lance"
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Data e Hora do Lance")
    is_valid = models.BooleanField(default=True, verbose_name="Lance Válido")

    class Meta:
        verbose_name = "Lance"
        verbose_name_plural = "Lances"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Lance de {self.user} no item {self.item} - R$ {self.amount:.2f}"

class Pagamento(models.Model):
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
    # ForeignKeys serão importadas mais tarde
    rural_item = models.ForeignKey(
        'auction_management.RuralItem',
        on_delete=models.CASCADE,
        related_name='pagamentos',
        verbose_name="Item Rural",
        null=True,
        blank=True
    )
    real_estate = models.ForeignKey(
        'auction_management.RealEstate',
        on_delete=models.CASCADE,
        related_name='pagamentos',
        verbose_name="Imóvel",
        null=True,
        blank=True
    )
    vehicle = models.ForeignKey(
        'auction_management.Vehicle',
        on_delete=models.CASCADE,
        related_name='pagamentos',
        verbose_name="Veículo",
        null=True,
        blank=True
    )
    other_goods = models.ForeignKey(
        'auction_management.OtherGoods',
        on_delete=models.CASCADE,
        related_name='pagamentos',
        verbose_name="Outro Bem",
        null=True,
        blank=True
    )
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
    def item_associado(self):
        """
        Retorna o item associado ao pagamento.
        """
        if self.rural_item:
            return self.rural_item
        elif self.real_estate:
            return self.real_estate
        elif self.vehicle:
            return self.vehicle
        elif self.other_goods:
            return self.other_goods
        return "Nenhum item associado"
