from django.contrib import admin
from .models import Bid, Payment

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    """
    Configuração do painel administrativo para o modelo Bid.
    """
    list_display = (
        'id', 'user', 'item_display', 'amount', 'timestamp', 'is_valid'
    )
    list_filter = ('is_valid', 'timestamp', )
    search_fields = ('user__username', 'user__email',)
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',)

    def item_display(self, obj):
        """
        Retorna uma representação amigável do item associado ao lance.
        """
        item_instance = obj.get_item_instance()
        return str(item_instance) if item_instance else "Item não encontrado"
    item_display.short_description = 'Item Relacionado'

    fieldsets = (
        ("Informações do Lance", {
            "fields": (
                'user', 'amount', 'is_valid', 'timestamp'
            )
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Configuração do painel administrativo para o modelo Payment.
    """
    list_display = (
        'id', 'user', 'item_display', 'amount', 'status', 'due_date', 'payment_date', 'created_at'
    )
    list_filter = ('status', 'due_date', 'created_at', 'content_type')
    search_fields = ('user__username', 'user__email', 'content_type__model', 'object_id')
    ordering = ('-due_date', '-created_at')
    date_hierarchy = 'due_date'
    readonly_fields = ('created_at', 'payment_date')

    def item_display(self, obj):
        """
        Retorna uma representação amigável do item associado ao pagamento.
        """
        item_instance = obj.get_item_instance
        return str(item_instance) if item_instance else "Item não encontrado"
    item_display.short_description = 'Item Relacionado'

    fieldsets = (
        ("Informações do Pagamento", {
            "fields": (
                'user', 'content_type', 'object_id', 'amount', 'status', 
                'payment_date', 'due_date', 'created_at'
            )
        }),
    )
