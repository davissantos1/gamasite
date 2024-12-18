from django.contrib import admin
from .models import Bid

# Admin para Lances
class BidAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'amount', 'timestamp', 'is_valid')
    list_filter = ('is_valid', 'timestamp')
    search_fields = ('item__codigo_item', 'user__username', 'amount')

admin.site.register(Bid, BidAdmin)