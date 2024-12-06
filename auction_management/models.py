from django.db import models
from django.utils.timezone import now
from django.conf import settings
from datetime import timedelta
import uuid
from categories.models import AuctionCategory

def default_auction_time():
    """Retorna a data e hora atual."""
    return now()

def generate_auction_code(auction):
    """Gera o código de leilão com base no nome do leilão e números aleatórios."""
    return f"{auction.descricao.replace(' ', '_').upper()}_{uuid.uuid4().hex[:8].upper()}"

def generate_item_code(item):
    """Gera o código do item com base no nome do item e números aleatórios."""
    return f"{item.nome.replace(' ', '_').upper()}_{uuid.uuid4().hex[:8].upper()}"

class Auction(models.Model):
    codigo_leilao = models.CharField(
        max_length=50,
        primary_key=True,  # Torna 'codigo_leilao' a chave primária
        verbose_name="Código do Leilão",
        unique=True
    )
    descricao = models.TextField(verbose_name="Descrição do Leilão")
    categoria = models.ForeignKey(
        AuctionCategory,
        on_delete=models.CASCADE,
        verbose_name="Categoria"
    )
    comitente = models.CharField(max_length=255, verbose_name="Comitente")
    complemento = models.TextField(blank=True, null=True, verbose_name="Complemento")
    active = models.BooleanField(default=True, verbose_name="Ativo")
    date_time = models.DateTimeField(
        verbose_name="Data e Hora do Leilão",
        default=now
    )
    duration_hours = models.PositiveIntegerField(
        default=2,
        verbose_name="Duração do Leilão (em horas)"
    )
    quantidade_lotes = models.PositiveIntegerField(
        default=0,
        verbose_name="Quantidade de Lotes"
    )

    def is_live(self):
        """Verifica se o leilão está ao vivo."""
        start = self.date_time
        end = start + timedelta(hours=self.duration_hours)
        return start <= now() <= end and self.active

    def save(self, *args, **kwargs):
        if not self.codigo_leilao:  # Gera o código do leilão se não existir
            self.codigo_leilao = generate_auction_code(self)
        if self.date_time + timedelta(hours=self.duration_hours) < now():
            self.active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Leilão {self.codigo_leilao}"

class BaseItem(models.Model):
    nome = models.CharField(
        max_length=255,
        verbose_name="Nome",
        default="Item"
    )
    descricao = models.TextField(verbose_name="Descrição", default="sem descrição")
    valor_avaliado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor Avaliado",
        default=0.00
    )
    codigo_item = models.CharField(
        max_length=50,  # Maior tamanho devido ao código gerado
        primary_key=True,  # Torna 'codigo_item' a chave primária
        verbose_name="Código do Item",
    )
    leilao = models.ForeignKey(
        'Auction',
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name='Leilão',
        null=True,
        blank=True
    )
    tipo_item = models.ForeignKey(
        'auction_management.ItemType',
        on_delete=models.CASCADE,
        verbose_name="Tipo do Item",
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        # Gera o código do item se não existir
        if not self.codigo_item:
            self.codigo_item = generate_item_code(self)
        
        # Associar automaticamente o tipo de item com base na categoria do leilão
        if self.leilao:
            if not self.tipo_item:
                if self.leilao.categoria.nome == 'Imóvel':
                    self.tipo_item = ItemType.objects.get(nome='Imóvel')
                elif self.leilao.categoria.nome == 'Veículo':
                    self.tipo_item = ItemType.objects.get(nome='Veículo')
                elif self.leilao.categoria.nome == 'Rural':
                    self.tipo_item = ItemType.objects.get(nome='Rural')
                elif self.leilao.categoria.nome == 'Outros Bens':
                    self.tipo_item = ItemType.objects.get(nome='Outros Bens')
                elif self.leilao.categoria.nome == 'Sem categoria':
                    self.tipo_item = ItemType.objects.get(nome='Sem categoria')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({self.codigo_item})"

    class Meta:
        abstract = True  # Este modelo permanece abstrato

class ItemType(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Tipo de Item", unique=True)
    descricao = models.TextField(verbose_name="Descrição", blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Tipo de Item"
        verbose_name_plural = "Tipos de Itens"

class Bid(models.Model):
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

class RuralItem(BaseItem):
    origem = models.CharField(max_length=50, default="Rural", verbose_name="Origem")

    leilao = models.ForeignKey(
        'Auction',
        on_delete=models.CASCADE,
        related_name='rural_items',  # Unique related name
        verbose_name='Leilão',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Item Rural - {self.tipo_item}"
    
    class Meta:
        # Não precisa de `id`, o Django usará `codigo_item` como chave primária
        pass


class RealEstate(BaseItem):
    quartos = models.IntegerField(verbose_name="Quartos")
    metragem = models.FloatField(verbose_name="Metragem")
    localizacao = models.CharField(max_length=255, verbose_name="Localização")
    estado_imovel = models.CharField(max_length=50, verbose_name="Estado do Imóvel")

    leilao = models.ForeignKey(
        'Auction',
        on_delete=models.CASCADE,
        related_name='real_estates',  # Unique related name
        verbose_name='Leilão',
        null=True,
        blank=True
    )
    class Meta:
        # Não precisa de `id`, o Django usará `codigo_item` como chave primária
        pass

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

    leilao = models.ForeignKey(
        'Auction',
        on_delete=models.CASCADE,
        related_name='vehicles',  # Unique related name
        verbose_name='Leilão',
        null=True,
        blank=True
    )
    class Meta:
        # Não precisa de `id`, o Django usará `codigo_item` como chave primária
        pass


class OtherGoods(BaseItem):
    localizacao = models.CharField(max_length=255, verbose_name="Localização")
    estado_item = models.CharField(max_length=50, verbose_name="Estado do Item")

    leilao = models.ForeignKey(
        'Auction',
        on_delete=models.CASCADE,
        related_name='other_goods',  # Unique related name
        verbose_name='Leilão',
        null=True,
        blank=True
    )
    class Meta:
        # Não precisa de `id`, o Django usará `codigo_item` como chave primária
        pass