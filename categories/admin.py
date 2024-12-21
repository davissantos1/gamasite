from django.contrib import admin
from .models import AuctionCategory

class AuctionCategoryAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    list_filter = ('nome',)
    search_fields = ('nome',)
    # Previne a criação de novas categorias, permitindo apenas as 4 definidas
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(nome__in=[AuctionCategory.IMOVEIS, AuctionCategory.VEICULOS, AuctionCategory.RURAL, AuctionCategory.OUTROS_BENS])

    def has_add_permission(self, request):
        return True  # Desabilita o botão de "Adicionar" novas categorias

    def has_change_permission(self, request, obj=None):
        return True  # Permite edição das categorias existentes

    def has_delete_permission(self, request, obj=None):
        return True  # Permite excluir categorias, se necessário

admin.site.register(AuctionCategory, AuctionCategoryAdmin)
