from django.db import models

class Auction(models.Model):
    lote = models.CharField(max_length=50, verbose_name="Lote")
    codigo_leilao = models.CharField(max_length=50, verbose_name="Código do Leilão")
    descricao = models.TextField(verbose_name="Descrição do Leilão")
    categoria = models.ForeignKey(
        'categories.AuctionCategory',  # Atualize com o nome correto do app e modelo
        on_delete=models.CASCADE,
        verbose_name="Categoria"
    )
    comitente = models.CharField(max_length=255, verbose_name="Comitente")
    complemento = models.TextField(blank=True, null=True, verbose_name="Complemento")

    def __str__(self):
        return f"Lote {self.lote} - Código {self.codigo_leilao}"


class BaseItem(models.Model):
    codigo_item = models.CharField(max_length=50, verbose_name="Código do Item")
    descricao = models.TextField(verbose_name="Descrição do Item")

    class Meta:
        abstract = False  


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
    valor_avaliado = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor Avaliado")
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
    valor_avaliado = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor Avaliado")
    localizacao = models.CharField(max_length=255, verbose_name="Localização")
    estado_item = models.CharField(max_length=50, verbose_name="Estado do Item")
