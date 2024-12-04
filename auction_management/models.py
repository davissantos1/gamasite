from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.conf import settings  # Para associar ao modelo de usuário
import uuid  

def default_auction_time():
    """Retorna a data e hora atual."""
    return now()

class Auction(models.Model):
    lote = models.CharField(max_length=50, verbose_name="Lote")
    codigo_leilao = models.CharField(max_length=50, verbose_name="Código do Leilão")
    descricao = models.TextField(verbose_name="Descrição do Leilão")
    categoria = models.ForeignKey(
        'categories.AuctionCategory',
        on_delete=models.CASCADE,
        verbose_name="Categoria"
    )
    comitente = models.CharField(max_length=255, verbose_name="Comitente")
    complemento = models.TextField(blank=True, null=True, verbose_name="Complemento")
    active = models.BooleanField(default=True, verbose_name="Ativo")
    date_time = models.DateTimeField(
        verbose_name="Data e Hora do Leilão",
        default=default_auction_time
    )
    duration_hours = models.PositiveIntegerField(
        default=2,
        verbose_name="Duração do Leilão (em horas)"
    )

    def is_live(self):
        """Verifica se o leilão está ao vivo."""
        start = self.date_time
        end = start + timedelta(hours=self.duration_hours)
        return start <= now() <= end and self.active

    def save(self, *args, **kwargs):
        # Atualiza automaticamente o status ativo
        if self.date_time + timedelta(hours=self.duration_hours) < now():
            self.active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Lote {self.lote} - Código {self.codigo_leilao}"


class BaseItem(models.Model):
    nome = models.CharField(
        max_length=255, 
        verbose_name="Nome", 
        default="Item"  
    )
    descricao = models.TextField()
    valor_avaliado = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Valor Avaliado", 
        default=0.00  # Adiciona valor padrão de 0
    )
    codigo_item = models.CharField(
        max_length=10,  # Ajuste o tamanho conforme necessário
        unique=True,
        verbose_name="Código do Item",
        default="",  # Será definido no `save` se vazio
        blank=True
    )

    def __str__(self):
        return f"{self.nome} ({self.codigo_item})"

    def save(self, *args, **kwargs):
        if not self.codigo_item:  # Gera um código se estiver vazio
            self.codigo_item = f"ITEM-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    class Meta:
        abstract = False



class Bid(models.Model):
    item = models.ForeignKey(
        BaseItem,
        on_delete=models.CASCADE,
        related_name="bids",
        verbose_name="Item do Leilão"
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
        ordering = ["-timestamp"]  # Ordena por data, mais recente primeiro

    def __str__(self):
        return f"Lance de {self.user} no item {self.item} - R$ {self.amount:.2f}"

class RuralItem(models.Model):
    origem = models.CharField(max_length=50, default="Rural", verbose_name="Origem")
    tipo_item = models.CharField(
        max_length=50,
        choices=[
            ("Imóvel", "Imóvel"),
            ("Veículo", "Veículo"),
            ("Outros Bens", "Outros Bens")
        ],
        verbose_name="Tipo do Item"
    )
    item = models.ForeignKey(
        BaseItem,
        on_delete=models.CASCADE,
        verbose_name="Item Associado",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Item Rural - {self.tipo_item}"


class RealEstate(BaseItem):
    quartos = models.IntegerField(verbose_name="Quartos")
    metragem = models.FloatField(verbose_name="Metragem")
    localizacao = models.CharField(max_length=255, verbose_name="Localização")
    estado_imovel = models.CharField(max_length=50, verbose_name="Estado do Imóvel")

class Vehicle(BaseItem):
    versao = models.CharField(max_length=100, verbose_name="Versão")
    fabricacao = models.IntegerField(verbose_name="Ano de Fabricação")
    marca = models.CharField(max_length=50, verbose_name="Marca")
    modelo = models.CharField(max_length=50, verbose_name="Modelo")
    categoria_veiculo = models.CharField(max_length=50, verbose_name="Categoria do Veículo")
    fipe = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor FIPE")
    tipo_documento = models.CharField(max_length=50, verbose_name="Tipo de Documento")
    tipo_monta = models.CharField(max_length=50, verbose_name="Tipo de Monta")
    tipo_chassi = models.CharField(max_length=50, verbose_name="Tipo de Chassi")
    blindado = models.BooleanField(default=False, verbose_name="Blindado")
    condicao = models.CharField(max_length=50, verbose_name="Condição")
    condicao_funcionamento = models.CharField(max_length=50, verbose_name="Condição de Funcionamento")
    numero_chassi = models.CharField(max_length=50, verbose_name="Número do Chassi")
    chave = models.BooleanField(default=False, verbose_name="Possui Chave")
    final_placa = models.CharField(max_length=1, verbose_name="Final da Placa")
    combustivel = models.CharField(max_length=50, verbose_name="Combustível")
    patio = models.CharField(max_length=100, verbose_name="Pátio")

class OtherGoods(BaseItem):
    localizacao = models.CharField(max_length=255, verbose_name="Localização")
    estado_item = models.CharField(max_length=50, verbose_name="Estado do Item")
