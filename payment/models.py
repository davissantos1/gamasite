from django.db import models
from django.conf import settings
from auction_management.models import RealEstate, Vehicle, RuralItem, OtherGoods

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
    # Relacionamento com RealEstate
    real_estate = models.ForeignKey(RealEstate, related_name='lances_realestate', on_delete=models.CASCADE, blank=True, null=True)
    
    # Relacionamento com Vehicle
    vehicle = models.ForeignKey(Vehicle, related_name='lances_vehicle', on_delete=models.CASCADE, blank=True, null=True)
    
    # Relacionamento com RuralItem
    rural_item = models.ForeignKey(RuralItem, related_name='lances_ruralitem', on_delete=models.CASCADE, blank=True, null=True)
    
    # Relacionamento com OtherGoods
    other_goods = models.ForeignKey(OtherGoods, related_name='lances_othergoods', on_delete=models.CASCADE, blank=True, null=True)

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
        """
        Retorna a string representando o lance, incluindo o item associado.
        """
        item_instance = self.get_item_instance()
        return f"Lance de {self.user} no item {item_instance} - R$ {self.amount:.2f}" if item_instance else f"Lance de {self.user} - R$ {self.amount:.2f}"

    def get_item_instance(self):
        """
        Retorna a instância concreta do item associado ao lance.
        """
        if self.real_estate:
            return self.real_estate
        elif self.vehicle:
            return self.vehicle
        elif self.rural_item:
            return self.rural_item
        elif self.other_goods:
            return self.other_goods
        return None

    @staticmethod
    def get_highest_bid(item_instance):
        """
        Retorna o lance com o maior valor para um determinado item (Imóvel, Veículo, Item Rural, Outros Bens).
        """
        if isinstance(item_instance, RealEstate):
            highest_bid = Bid.objects.filter(real_estate=item_instance).order_by('-amount').first()
        elif isinstance(item_instance, Vehicle):
            highest_bid = Bid.objects.filter(vehicle=item_instance).order_by('-amount').first()
        elif isinstance(item_instance, RuralItem):
            highest_bid = Bid.objects.filter(rural_item=item_instance).order_by('-amount').first()
        elif isinstance(item_instance, OtherGoods):
            highest_bid = Bid.objects.filter(other_goods=item_instance).order_by('-amount').first()
        else:
            highest_bid = None
        return highest_bid




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
    # Relacionamento com RealEstate
    real_estate = models.ForeignKey(RealEstate, related_name='pagamentos_realestate', on_delete=models.CASCADE, blank=True, null=True)
    
    # Relacionamento com Vehicle
    vehicle = models.ForeignKey(Vehicle, related_name='pagamentos_vehicle', on_delete=models.CASCADE, blank=True, null=True)
    
    # Relacionamento com RuralItem
    rural_item = models.ForeignKey(RuralItem, related_name='pagamentos_ruralitem', on_delete=models.CASCADE, blank=True, null=True)
    
    # Relacionamento com OtherGoods
    other_goods = models.ForeignKey(OtherGoods, related_name='pagamentos_othergoods', on_delete=models.CASCADE, blank=True, null=True)

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
        """
        Retorna a string representando o pagamento, incluindo o item associado.
        """
        item_instance = self.get_item_instance()
        return f"Pagamento de {self.user} - R$ {self.amount:.2f} - Status: {self.get_status_display()} - Item: {item_instance}" if item_instance else f"Pagamento de {self.user} - R$ {self.amount:.2f} - Status: {self.get_status_display()}"

    def get_item_instance(self):
        """
        Retorna a instância concreta do item associado ao pagamento.
        """
        if self.real_estate:
            return self.real_estate
        elif self.vehicle:
            return self.vehicle
        elif self.rural_item:
            return self.rural_item
        elif self.other_goods:
            return self.other_goods
        return None
