from django.contrib import admin
from .models import Auction, RealEstate, Vehicle, OtherGoods, RuralItem, Bid, ItemType, generate_auction_code, generate_item_code
from django.conf import settings
from django.utils.html import format_html
from django.core.exceptions import ValidationError

# Admin para Leilões
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('codigo_leilao', 'descricao', 'categoria', 'comitente', 'quantidade_lotes', 'date_time', 'active', 'imagem_tag')
    list_filter = ('active', 'categoria', 'date_time')
    search_fields = ('codigo_leilao', 'descricao', 'comitente')
    readonly_fields = ('codigo_leilao',)

    def imagem_tag(self, obj):
        if obj.imagem:
            return format_html(f'<img src="{obj.imagem.url}" width="50" height="50"/>')
        return format_html(f'<img src="{settings.MEDIA_URL}default/default_image.jpg" width="50" height="50"/>')

    imagem_tag.short_description = 'Imagem'

    def save_model(self, request, obj, form, change):
        if not obj.codigo_leilao:
            obj.codigo_leilao = generate_auction_code(obj)
        super().save_model(request, obj, form, change)

    def numero_de_itens(self, obj):
        total_itens = obj.real_estates.count() + obj.rural_items.count() + obj.vehicles.count() + obj.other_goods.count()
        return total_itens
    numero_de_itens.short_description = "Número de Itens"

admin.site.register(Auction, AuctionAdmin)

# Base para Itens
class ItemAdmin(admin.ModelAdmin):
    list_display = ('codigo_item', 'nome', 'valor_avaliado', 'imagem_tag')
    search_fields = ('codigo_item', 'nome')
    readonly_fields = ('codigo_item',)

    # Adicionando o campo de imagem no formulário do admin
    fieldsets = (
        (None, {
            'fields': ('nome', 'valor_avaliado', 'imagem')  # Adicionando o campo de imagem
        }),
        ('Informações adicionais', {
            'fields': ('descricao', 'leilao', 'tipo_item'),  # Outros campos que você pode querer adicionar
        }),
    )

    def imagem_tag(self, obj):
        if obj.imagem:
            return format_html(f'<img src="{obj.imagem.url}" width="50" height="50"/>')
        return format_html(f'<img src="{settings.MEDIA_URL}default/default_image.jpg" width="50" height="50"/>')

    imagem_tag.short_description = 'Imagem'

    def save_model(self, request, obj, form, change):
        if not obj.codigo_item:
            obj.codigo_item = generate_item_code(obj)
        
        # Lógica de atribuição do tipo de item de acordo com a categoria do leilão
        if obj.leilao:
            categoria = obj.leilao.categoria.nome
            if categoria == 'Veículo' and obj.tipo_item.nome != 'Veículo':
                obj.tipo_item = ItemType.objects.get(nome='Veículo')
            elif categoria == 'Imóvel' and obj.tipo_item.nome != 'Imóvel':
                obj.tipo_item = ItemType.objects.get(nome='Imóvel')
            elif categoria == 'Rural' and obj.tipo_item.nome not in ['Imóvel', 'Veículo', 'Outros']:
                raise ValidationError('Para a categoria Rural, o tipo de item deve ser Imóvel, Veículo ou Outros.')
            elif categoria == 'Outros Bens' and obj.tipo_item.nome != 'Outros':
                obj.tipo_item = ItemType.objects.get(nome='Outros')
        
        super().save_model(request, obj, form, change)

# Admin para Imóveis
class RealEstateAdmin(ItemAdmin):
    list_display = ('codigo_item', 'nome', 'valor_avaliado', 'imagem_tag', 'descricao')
    search_fields = ('codigo_item', 'nome')

    fieldsets = (
        (None, {
            'fields': ('nome', 'valor_avaliado', 'imagem', 'descricao')  # Adicionando o campo de imagem e outros específicos de imóveis
        }),
        ('Informações adicionais', {
            'fields': ('leilao', 'tipo_item'),
        }),
    )

admin.site.register(RealEstate, RealEstateAdmin)

# Admin para Veículos
class VehicleAdmin(ItemAdmin):
    list_display = ('codigo_item', 'nome', 'marca', 'modelo', 'fabricacao', 'fipe', 'valor_avaliado', 'imagem_tag')
    search_fields = ('codigo_item', 'nome', 'marca', 'modelo')

    fieldsets = (
        (None, {
            'fields': ('nome', 'marca', 'modelo', 'fabricacao', 'fipe', 'valor_avaliado', 'imagem')  # Campos específicos para veículos
        }),
        ('Informações adicionais', {
            'fields': ('leilao', 'tipo_item'),
        }),
    )

admin.site.register(Vehicle, VehicleAdmin)

# Admin para Outros Bens
class OtherGoodsAdmin(ItemAdmin):
    list_display = ('codigo_item', 'nome', 'valor_avaliado', 'leilao', 'status_lote', 'status_pagamento', 'imagem_tag')
    search_fields = ('codigo_item', 'nome')

    fieldsets = (
        (None, {
            'fields': ('nome', 'valor_avaliado', 'imagem', 'descricao')  # Campos específicos para outros bens
        }),
        ('Informações adicionais', {
            'fields': ('leilao', 'status_lote', 'status_pagamento', 'tipo_item'),
        }),
    )

admin.site.register(OtherGoods, OtherGoodsAdmin)

# Admin para Itens Rurais
class RuralItemAdmin(ItemAdmin):
    list_display = ('codigo_item', 'nome', 'valor_avaliado', 'leilao', 'status_lote', 'status_pagamento', 'imagem_tag')
    search_fields = ('codigo_item', 'nome')

    fieldsets = (
        (None, {
            'fields': ('nome', 'valor_avaliado', 'imagem', 'descricao')  # Campos específicos para itens rurais
        }),
        ('Informações adicionais', {
            'fields': ('leilao', 'status_lote', 'status_pagamento', 'tipo_item'),
        }),
    )

admin.site.register(RuralItem, RuralItemAdmin)

# Admin para Lances
class BidAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'amount', 'timestamp', 'is_valid')
    list_filter = ('is_valid', 'timestamp')
    search_fields = ('item__codigo_item', 'user__username', 'amount')

admin.site.register(Bid, BidAdmin)

# Admin para Tipos de Item
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

admin.site.register(ItemType, ItemTypeAdmin)
