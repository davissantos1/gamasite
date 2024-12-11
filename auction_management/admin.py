from django.contrib import admin
from .models import Auction, RealEstate, Vehicle, OtherGoods, Bid, generate_auction_code
from django.conf import settings
from django.utils.html import format_html

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('codigo_leilao', 'descricao', 'categoria', 'comitente', 'quantidade_lotes', 'date_time', 'active', 'imagem_tag')
    list_filter = ('active', 'categoria', 'date_time')
    search_fields = ('codigo_leilao', 'descricao', 'comitente')
    readonly_fields = ('codigo_leilao',)  # Código gerado automaticamente

    def imagem_tag(self, obj):
        if obj.imagem:
            return format_html(f'<img src="{obj.imagem.url}" width="50" height="50"/>')
        return format_html(f'<img src="{settings.MEDIA_URL}default/default_image.jpg" width="50" height="50"/>')
    
    imagem_tag.short_description = 'Imagem'

    def save_model(self, request, obj, form, change):
        """Gera o código do leilão automaticamente se não existir."""
        if not obj.codigo_leilao:
            obj.codigo_leilao = generate_auction_code(obj)
        super().save_model(request, obj, form, change)

admin.site.register(Auction, AuctionAdmin)

class RealEstateAdmin(admin.ModelAdmin):
    list_display = ('codigo_item', 'nome', 'valor_avaliado')  
    search_fields = ('codigo_item', 'nome')

admin.site.register(RealEstate, RealEstateAdmin)

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('codigo_item', 'nome', 'marca', 'modelo', 'fabricacao', 'fipe', 'valor_avaliado')
    search_fields = ('codigo_item', 'nome', 'marca', 'modelo')

admin.site.register(Vehicle, VehicleAdmin)

class OtherGoodsAdmin(admin.ModelAdmin):
    list_display = ('codigo_item', 'nome', 'valor_avaliado', 'leilao', 'status_lote', 'status_pagamento')  
    search_fields = ('codigo_item', 'nome')

admin.site.register(OtherGoods, OtherGoodsAdmin)

class BidAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'amount', 'timestamp', 'is_valid')
    list_filter = ('is_valid', 'timestamp')
    search_fields = ('item__codigo_item', 'user__username', 'amount')

admin.site.register(Bid, BidAdmin)
