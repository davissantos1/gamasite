from django.contrib import admin
from .models import Auction, Bid, BaseItem

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('lote', 'codigo_leilao', 'categoria', 'comitente', 'date_time', 'active')
    list_editable = ('active',)
    search_fields = ('lote', 'codigo_leilao', 'descricao')
    list_filter = ('categoria', 'active', 'date_time')

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ("item", "user", "amount", "timestamp", "is_valid")
    list_filter = ("is_valid", "timestamp")
    search_fields = ("item__name", "user__username", "amount")

@admin.register(BaseItem)
class BaseItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'valor_avaliado')