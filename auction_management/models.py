from django.db import models
from django.utils.timezone import now
from django.conf import settings
from datetime import timedelta
import uuid
from categories.models import AuctionCategory
from decimal import Decimal


def default_auction_time():
    """Retorna a data e hora atual."""
    return now()

def generate_auction_code(auction):
    """Gera o código de leilão com base no nome do leilão e números aleatórios."""
    return f"{auction.comitente.replace(' ', '_').upper()}_{uuid.uuid4().hex[:8].upper()}"

def generate_item_code(item):
    """Gera o código do item com base no nome do item e números aleatórios."""
    return f"{item.nome.replace(' ', '_').upper()}_{uuid.uuid4().hex[:8].upper()}"

def generate_item_image_path(instance, filename):
    """Gera o caminho dinâmico para upload das imagens do item."""
    if instance.vehicle:
        leilao_codigo = instance.vehicle.leilao.codigo_leilao if instance.vehicle.leilao else "sem_leilao"
        item_codigo = instance.vehicle.codigo_item
        tipo_item = "veiculo"
    elif instance.real_estate:
        leilao_codigo = instance.real_estate.leilao.codigo_leilao if instance.real_estate.leilao else "sem_leilao"
        item_codigo = instance.real_estate.codigo_item
        tipo_item = "imovel"
    elif instance.rural_item:
        leilao_codigo = instance.rural_item.leilao.codigo_leilao if instance.rural_item.leilao else "sem_leilao"
        item_codigo = instance.rural_item.codigo_item
        tipo_item = "rural"
    elif instance.other_goods:
        leilao_codigo = instance.other_goods.leilao.codigo_leilao if instance.other_goods.leilao else "sem_leilao"
        item_codigo = instance.other_goods.codigo_item
        tipo_item = "outros_bens"
    else:
        leilao_codigo = "sem_leilao"
        item_codigo = "sem_codigo_item"
        tipo_item = "sem_tipo"

    return f"imagens/{tipo_item}/{leilao_codigo}/{item_codigo}/{filename}"

def generate_item_thumb_path(instance, filename):
    """Gera o caminho dinâmico para o upload de thumbnails."""
    if isinstance(instance, Vehicle):
        leilao_codigo = instance.leilao.codigo_leilao if instance.leilao else "sem_leilao"
        item_codigo = instance.codigo_item
        tipo_item = "veiculo"
    elif isinstance(instance, RealEstate):
        leilao_codigo = instance.leilao.codigo_leilao if instance.leilao else "sem_leilao"
        item_codigo = instance.codigo_item
        tipo_item = "imovel"
    elif isinstance(instance, RuralItem):
        leilao_codigo = instance.leilao.codigo_leilao if instance.leilao else "sem_leilao"
        item_codigo = instance.codigo_item
        tipo_item = "rural"
    elif isinstance(instance, OtherGoods):
        leilao_codigo = instance.leilao.codigo_leilao if instance.leilao else "sem_leilao"
        item_codigo = instance.codigo_item
        tipo_item = "outros_bens"
    else:
        leilao_codigo = "sem_leilao"
        item_codigo = "sem_codigo_item"
        tipo_item = "sem_tipo"

    return f"thumbnail/{tipo_item}/{leilao_codigo}/{item_codigo}/{filename}"


def generate_auction_thumb_path(instance, filename):
    """Gera o caminho dinâmico para o upload de thumbnails."""
    if isinstance(instance, Auction):
        leilao_codigo = instance.codigo_leilao 
    else:
        leilao_codigo = "sem_codigo"

    return f"thumbnail/leilao/{leilao_codigo}/{filename}"

class Auction(models.Model):
    STATUS_CHOICES = [
        ('programado', 'Programado'),
        ('ao_vivo', 'Ao Vivo'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]
    
    codigo_leilao = models.CharField(
        max_length=50,
        primary_key=True,
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
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='programado',  # Valor padrão para quando o leilão ainda estiver programado
        verbose_name="Status do Leilão"
    )
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
    thumbnail = models.ImageField(upload_to=generate_auction_thumb_path, default='default/default_image.jpg')
    documento_editais = models.FileField(upload_to='editais/', null=True, blank=True, verbose_name="Documento Edital (PDF)")
    ao_vivo_iniciado = models.BooleanField(default=False, verbose_name="Leilão Ao Vivo Iniciado")

    @property
    def is_scheduled_for_today(self):
        """Verifica se o leilão está programado para hoje."""
        today = now().date()
        return self.date_time.date() == today and self.date_time > now() and self.status == 'programado'

    def save(self, *args, **kwargs):
        if not self.codigo_leilao:  # Gera o código do leilão se não existir
            self.codigo_leilao = generate_auction_code(self)

        # Determina o status do leilão com base na data e hora
        if self.date_time + timedelta(hours=self.duration_hours) < now():
            self.status = 'finalizado'
        elif self.date_time <= now() < (self.date_time + timedelta(hours=self.duration_hours)):
            self.status = 'ao_vivo'
        elif self.date_time > now():
            self.status = 'programado'
        
        # Verifica o número total de itens associados ao leilão
        total_items = (
            self.vehicles.count() + 
            self.real_estates.count() + 
            self.other_goods.count() + 
            self.rural_items.count()
        )

        if total_items > self.quantidade_lotes:
            raise ValueError("O número de itens associados excede a quantidade de lotes definida.")
    
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Leilão {self.codigo_leilao}"

    class Meta:
        verbose_name = "Leilão"
        verbose_name_plural = "Leilões"


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
    valor_inicial = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor Inicial",
        null=True,
        blank=True
    )
    codigo_item = models.CharField(
        max_length=50,
        primary_key=True,
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
    valor_arrematado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor Arrematado",
        null=True,
        blank=True
    )
    status_lote = models.CharField(
        max_length=50,
        choices=[('aceitando_lances', 'Aceitando lances'), ('arrematado', 'Arrematado'), ('pendente_de_pagamento', 'Pendente de pagamento')],
        default='aceitando_lances',
        verbose_name="Status do Lote"
    )
    status_pagamento = models.CharField(
        max_length=50,
        choices=[('pendente', 'Pendente'), ('pago', 'Pago')],
        default='pendente',
        verbose_name="Status de Pagamento"
    )
    destacado = models.BooleanField(
        default=False,
        verbose_name="Item Destacado"
    )

    def save(self, *args, **kwargs):
        if not self.codigo_item:
            self.codigo_item = generate_item_code(self)

        # Verifica e define o valor inicial como 50% do valor avaliado
        if self.valor_avaliado and self.valor_inicial is None:
            self.valor_inicial = self.valor_avaliado * Decimal('0.5')

        # Inicializa a variável total_items
        total_items = 0

        if self.leilao:
            total_items = (
                self.leilao.vehicles.count() +
                self.leilao.real_estates.count() +
                self.leilao.other_goods.count() +
                self.leilao.rural_items.count()
            )

        # Verifica se o número de itens excede a quantidade de lotes permitidos
        if total_items >= self.leilao.quantidade_lotes:
            raise ValueError("Este leilão já atingiu o número máximo de itens permitido.")

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
        abstract = True

class ItemImage(models.Model):
    imagem = models.ImageField(upload_to=generate_item_image_path, verbose_name="Imagem do Item")
    descricao = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descrição da Imagem")

    # Relacionamento com RealEstate
    real_estate = models.ForeignKey('RealEstate', related_name='imagens_realestate', on_delete=models.CASCADE, blank=True, null=True)
    
    # Relacionamento com Vehicle
    vehicle = models.ForeignKey('Vehicle', related_name='imagens_vehicle', on_delete=models.CASCADE, blank=True, null=True)
    
    # Relacionamento com RuralItem
    rural_item = models.ForeignKey('RuralItem', related_name='imagens_ruralitem', on_delete=models.CASCADE, blank=True, null=True)
    
    # Relacionamento com OtherGoods
    other_goods = models.ForeignKey('OtherGoods', related_name='imagens_othergoods', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.descricao if self.descricao else f"Imagem {self.id}"

    class Meta:
        verbose_name = "Imagem do Item"
        verbose_name_plural = "Imagens dos Itens"

class ItemType(models.Model):
    VEICULO = 'Veículo'
    IMOVEL = 'Imóvel'
    OUTROS = 'Outros'

    ITEM_TYPE_CHOICES = [
        (VEICULO, 'Veículo'),
        (IMOVEL, 'Imóvel'),
        (OUTROS, 'Outros'),
    ]

    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do Tipo de Item",
        choices=ITEM_TYPE_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Tipo de Item"
        verbose_name_plural = "Tipos de Itens"

class RuralItem(BaseItem):
    thumbnail = models.ImageField(upload_to=generate_item_thumb_path, default='default/default_image.jpg')  
    origem = models.CharField(max_length=50, default="Rural", verbose_name="Origem")
    leilao = models.ForeignKey(
        'Auction',
        on_delete=models.CASCADE,
        related_name='rural_items',  # Ajustado para ser único
        verbose_name='Leilão',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Item Rural - {self.tipo_item}"
    
    class Meta:
        verbose_name = "Item Rural"
        verbose_name_plural = "Itens Rurais"


class RealEstate(BaseItem):
    thumbnail = models.ImageField(upload_to=generate_item_thumb_path, default='default/default_image.jpg') 
    quartos = models.IntegerField(verbose_name="Quartos")
    metragem = models.FloatField(verbose_name="Metragem")
    localizacao = models.CharField(max_length=255, verbose_name="Localização")
    estado_imovel = models.CharField(max_length=50, verbose_name="Estado do Imóvel")
   
    leilao = models.ForeignKey(
        'Auction',
        on_delete=models.CASCADE,
        related_name='real_estates',  # Ajustado para ser único
        verbose_name='Leilão',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Imóvel"
        verbose_name_plural = "Imóveis"


class Vehicle(BaseItem):
    thumbnail = models.ImageField(upload_to=generate_item_thumb_path, default='default/default_image.jpg')
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
        related_name='vehicles',  # Ajustado para ser único
        verbose_name='Leilão',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"


class OtherGoods(BaseItem):
    thumbnail = models.ImageField(upload_to=generate_item_thumb_path, default='default/default_image.jpg')
    
    leilao = models.ForeignKey(
        'Auction',
        on_delete=models.CASCADE,
        related_name='other_goods',  # Ajustado para ser único
        verbose_name='Leilão',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Outros Bens - {self.tipo_item}"

    class Meta:
        verbose_name = "Outro Bem"
        verbose_name_plural = "Outros Bens"