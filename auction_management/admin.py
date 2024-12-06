from django.contrib import admin
from .models import Auction, RealEstate, Vehicle, OtherGoods, Bid

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('codigo_leilao', 'descricao', 'categoria', 'comitente', 'quantidade_lotes', 'date_time', 'active')
    list_filter = ('active', 'categoria', 'date_time')
    search_fields = ('codigo_leilao', 'descricao', 'comitente')

admin.site.register(Auction, AuctionAdmin)

class RealEstateAdmin(admin.ModelAdmin):
    list_display = ('codigo_item', 'nome', 'localizacao', 'metragem', 'estado_imovel', 'valor_avaliado')
    search_fields = ('codigo_item', 'nome', 'localizacao')

admin.site.register(RealEstate, RealEstateAdmin)

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('codigo_item', 'nome', 'marca', 'modelo', 'fabricacao', 'fipe', 'valor_avaliado')
    search_fields = ('codigo_item', 'nome', 'marca', 'modelo')

admin.site.register(Vehicle, VehicleAdmin)

class OtherGoodsAdmin(admin.ModelAdmin):
    list_display = ('codigo_item', 'nome', 'localizacao', 'estado_item', 'valor_avaliado')
    search_fields = ('codigo_item', 'nome', 'localizacao')

admin.site.register(OtherGoods, OtherGoodsAdmin)

class BidAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'amount', 'timestamp', 'is_valid')
    list_filter = ('is_valid', 'timestamp')
    search_fields = ('item__codigo_item', 'user__username', 'amount')

admin.site.register(Bid, BidAdmin)
