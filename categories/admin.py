from django.contrib import admin
from .models import AuctionCategory

@admin.register(AuctionCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'descricao')
