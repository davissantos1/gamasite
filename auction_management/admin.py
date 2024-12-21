from django.contrib import admin
from .models import Auction, RealEstate, Vehicle, OtherGoods, RuralItem, ItemType, ItemImage
from django.conf import settings
from django.utils.html import format_html

# Configuração Base para Customizações
class BaseAdmin(admin.ModelAdmin):
    def imagem_tag(self, obj):
        if obj.thumbnail:
            return format_html(f'<img src="{obj.thumbnail.url}" style="width: 60px; height: 60px; border-radius: 5px;"/>')
        return format_html(f'<img src="{settings.MEDIA_URL}default/default_image.jpg" style="width: 60px; height: 60px; border-radius: 5px;"/>')

    imagem_tag.short_description = 'Thumbnail'

# Inline para Imagens
class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1
    fields = ('imagem', 'descricao')
    readonly_fields = ('imagem_preview',)

    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html(f'<img src="{obj.imagem.url}" style="width: 100px; height: auto;"/>')
        return "Sem imagem"

    imagem_preview.short_description = 'Pré-visualização'

# Admin para Leilões
class AuctionAdmin(BaseAdmin):
    list_display = ('codigo_leilao', 'descricao', 'categoria', 'comitente', 'quantidade_lotes', 'date_time', 'active', 'numero_de_itens', 'imagem_tag')
    list_filter = ('active', 'categoria', 'date_time')
    search_fields = ('codigo_leilao', 'descricao', 'comitente')
    readonly_fields = ('codigo_leilao',)
    ordering = ('-date_time',)

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('codigo_leilao', 'descricao', 'categoria', 'comitente', 'quantidade_lotes', 'active', 'thumbnail')
        }),
        ('Datas', {
            'fields': ('date_time',),
        }),
    )

    def numero_de_itens(self, obj):
        total_itens = obj.real_estates.count() + obj.rural_items.count() + obj.vehicles.count() + obj.other_goods.count()
        return total_itens

    numero_de_itens.short_description = "Número de Itens"

admin.site.register(Auction, AuctionAdmin)

# Admin para Real Estate
class RealEstateAdmin(BaseAdmin):
    list_display = ('codigo_item', 'nome', 'valor_avaliado', 'localizacao', 'estado_imovel', 'leilao', 'status_lote', 'status_pagamento', 'imagem_tag')
    search_fields = ('codigo_item', 'nome', 'localizacao')
    readonly_fields = ('codigo_item',)
    ordering = ('-valor_avaliado',)

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'valor_avaliado', 'thumbnail', 'destacado')
        }),
        ('Detalhes do Imóvel', {
            'fields': ('quartos', 'metragem', 'localizacao', 'estado_imovel'),
        }),
        ('Relacionamentos', {
            'fields': ('leilao', 'tipo_item', 'status_lote', 'status_pagamento'),
        }),
    )

    inlines = [ItemImageInline]

admin.site.register(RealEstate, RealEstateAdmin)

# Admin para Veículos
class VehicleAdmin(BaseAdmin):
    list_display = ('codigo_item', 'nome', 'valor_avaliado', 'modelo', 'fabricacao',  'leilao', 'status_lote', 'status_pagamento', 'imagem_tag')
    search_fields = ('codigo_item', 'nome', 'marca', 'modelo', 'patio')
    readonly_fields = ('codigo_item',)
    ordering = ('-fabricacao',)

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'valor_avaliado', 'thumbnail', 'destacado')
        }),
        ('Detalhes do Veículo', {
            'fields': ('marca', 'modelo', 'fabricacao', 'categoria_veiculo', 'combustivel', 'blindado', 'patio', 'fipe'),
        }),
        ('Relacionamentos', {
            'fields': ('leilao', 'tipo_item', 'status_lote', 'status_pagamento'),
        }),
    )

    inlines = [ItemImageInline]

admin.site.register(Vehicle, VehicleAdmin)

# Admin para Itens Rurais
class RuralItemAdmin(BaseAdmin):
    list_display = ('codigo_item', 'nome', 'valor_avaliado', 'origem', 'leilao', 'status_lote', 'status_pagamento', 'imagem_tag')
    search_fields = ('codigo_item', 'nome')
    readonly_fields = ('codigo_item',)
    ordering = ('-valor_avaliado',)

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'valor_avaliado', 'thumbnail', 'destacado')
        }),
        ('Relacionamentos', {
            'fields': ('origem', 'leilao', 'tipo_item', 'status_lote', 'status_pagamento'),
        }),
    )

    inlines = [ItemImageInline]

admin.site.register(RuralItem, RuralItemAdmin)

# Admin para Outros Bens
class OtherGoodsAdmin(BaseAdmin):
    list_display = ('codigo_item', 'nome', 'valor_avaliado', 'leilao', 'status_lote', 'status_pagamento', 'imagem_tag')
    search_fields = ('codigo_item', 'nome')
    readonly_fields = ('codigo_item',)
    ordering = ('-valor_avaliado',)

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'valor_avaliado', 'thumbnail', 'destacado')
        }),
        ('Relacionamentos', {
            'fields': ('leilao', 'tipo_item', 'status_lote', 'status_pagamento'),
        }),
    )

    inlines = [ItemImageInline]

admin.site.register(OtherGoods, OtherGoodsAdmin)

# Admin para Tipos de Item
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    ordering = ('nome',)

admin.site.register(ItemType, ItemTypeAdmin)
