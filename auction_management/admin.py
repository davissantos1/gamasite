from django.contrib import admin
from .models import Auction, RealEstate, Vehicle, OtherGoods, RuralItem, ItemType
from django.conf import settings
from django.utils.html import format_html


# Admin para Leilões
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('codigo_leilao', 'descricao', 'categoria', 'comitente', 'quantidade_lotes', 'date_time', 'active', 'numero_de_itens', 'imagem_tag')
    list_filter = ('active', 'categoria', 'date_time')
    search_fields = ('codigo_leilao', 'descricao', 'comitente')
    readonly_fields = ('codigo_leilao',)

    def imagem_tag(self, obj):
        if obj.imagem:
            return format_html(f'<img src="{obj.imagem.url}" width="50" height="50"/>')
        return format_html(f'<img src="{settings.MEDIA_URL}default/default_image.jpg" width="50" height="50"/>')

    imagem_tag.short_description = 'Imagem'

    def numero_de_itens(self, obj):
        total_itens = obj.real_estates.count() + obj.rural_items.count() + obj.vehicles.count() + obj.other_goods.count()
        return total_itens

    numero_de_itens.short_description = "Número de Itens"

admin.site.register(Auction, AuctionAdmin)


# Admin personalizado para RealEstate
class RealEstateAdmin(admin.ModelAdmin):
    list_display = ('codigo_item', 'nome', 'valor_avaliado', 'quartos', 'metragem', 'localizacao', 'estado_imovel', 'leilao', 'status_lote', 'status_pagamento', 'imagem_tag')
    search_fields = ('codigo_item', 'nome', 'localizacao')
    readonly_fields = ('codigo_item',)

    fieldsets = (
        (None, {
            'fields': ('nome', 'descricao', 'valor_avaliado', 'imagem', 'destacado')
        }),
        ('Informações do Imóvel', {
            'fields': ('quartos', 'metragem', 'localizacao', 'estado_imovel'),
        }),
        ('Informações adicionais', {
            'fields': ('leilao', 'tipo_item', 'status_lote', 'status_pagamento'),
        }),
    )

    def imagem_tag(self, obj):
        if obj.imagem:
            return format_html(f'<img src="{obj.imagem.url}" width="50" height="50"/>')
        return format_html(f'<img src="{settings.MEDIA_URL}default/default_image.jpg" width="50" height="50"/>')

    imagem_tag.short_description = 'Imagem'

admin.site.register(RealEstate, RealEstateAdmin)


# Admin personalizado para Vehicle
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('codigo_item', 'nome', 'valor_avaliado', 'marca', 'modelo', 'fabricacao', 'categoria_veiculo', 'combustivel', 'blindado', 'patio', 'leilao', 'status_lote', 'status_pagamento', 'imagem_tag')
    search_fields = ('codigo_item', 'nome', 'marca', 'modelo', 'patio')
    readonly_fields = ('codigo_item',)

    fieldsets = (
        (None, {
            'fields': ('nome', 'descricao', 'valor_avaliado', 'imagem', 'destacado')
        }),
        ('Informações do Veículo', {
            'fields': ('marca', 'modelo', 'fabricacao', 'categoria_veiculo', 'combustivel', 'blindado', 'patio'),
        }),
        ('Informações adicionais', {
            'fields': ('leilao', 'tipo_item', 'status_lote', 'status_pagamento'),
        }),
    )

    def imagem_tag(self, obj):
        if obj.imagem:
            return format_html(f'<img src="{obj.imagem.url}" width="50" height="50"/>')
        return format_html(f'<img src="{settings.MEDIA_URL}default/default_image.jpg" width="50" height="50"/>')

    imagem_tag.short_description = 'Imagem'

admin.site.register(Vehicle, VehicleAdmin)



# Admin personalizado para RuralItem
class RuralItemAdmin(admin.ModelAdmin):
    list_display = ('codigo_item', 'nome', 'valor_avaliado', 'origem', 'leilao', 'status_lote', 'status_pagamento', 'imagem_tag')
    search_fields = ('codigo_item', 'nome')
    readonly_fields = ('codigo_item',)

    fieldsets = (
        (None, {
            'fields': ('nome', 'descricao', 'valor_avaliado', 'imagem', 'destacado')
        }),
        ('Informações adicionais', {
            'fields': ('origem', 'leilao', 'tipo_item', 'status_lote', 'status_pagamento'),
        }),
    )

    def imagem_tag(self, obj):
        if obj.imagem:
            return format_html(f'<img src="{obj.imagem.url}" width="50" height="50"/>')
        return format_html(f'<img src="{settings.MEDIA_URL}default/default_image.jpg" width="50" height="50"/>')

    imagem_tag.short_description = 'Imagem'

admin.site.register(RuralItem, RuralItemAdmin)


# Admin personalizado para OtherGoods
class OtherGoodsAdmin(admin.ModelAdmin):
    list_display = ('codigo_item', 'nome', 'valor_avaliado', 'leilao', 'status_lote', 'status_pagamento', 'imagem_tag')
    search_fields = ('codigo_item', 'nome')
    readonly_fields = ('codigo_item',)

    fieldsets = (
        (None, {
            'fields': ('nome', 'descricao', 'valor_avaliado', 'imagem', 'destacado')
        }),
        ('Informações adicionais', {
            'fields': ('leilao', 'tipo_item', 'status_lote', 'status_pagamento'),
        }),
    )

    def imagem_tag(self, obj):
        if obj.imagem:
            return format_html(f'<img src="{obj.imagem.url}" width="50" height="50"/>')
        return format_html(f'<img src="{settings.MEDIA_URL}default/default_image.jpg" width="50" height="50"/>')

    imagem_tag.short_description = 'Imagem'

admin.site.register(OtherGoods, OtherGoodsAdmin)


# Admin para Tipos de Item
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

admin.site.register(ItemType, ItemTypeAdmin)
