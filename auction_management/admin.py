from django.contrib import admin
from .models import Auction, Vehicle, RealEstate, RuralItem, OtherGoods, ItemImage, ItemType
from django.utils.html import format_html
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
import locale

# Definir a localidade para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

from django.contrib import admin

class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 0  # Garante que sempre haja uma linha em branco para criar novas instâncias
    fields = ('imagem',)  # Inclui o campo de descrição
    readonly_fields = ()  # Define campos somente leitura se necessário

    def save_new_instance(self, obj, parent_instance):
        """Associa a nova imagem ao modelo pai correto."""
        if isinstance(parent_instance, Vehicle):
            obj.vehicle = parent_instance
        elif isinstance(parent_instance, RealEstate):
            obj.real_estate = parent_instance
        elif isinstance(parent_instance, RuralItem):
            obj.rural_item = parent_instance
        elif isinstance(parent_instance, OtherGoods):
            obj.other_goods = parent_instance
        obj.save()

    def save_formset(self, request, form, formset, change):
        """Sobrescreve a lógica de salvar para associar corretamente a imagem."""
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk:  # Verifica se é uma nova instância
                self.save_new_instance(instance, form.instance)
        formset.save_m2m()  # Salva as relações ManyToMany

    def get_formset(self, request, obj=None, **kwargs):
        """Permite configurar o parent_model_instance e garantir que o formset sempre crie novas instâncias."""
        self.parent_model_instance = obj

        # Não faz alterações no queryset, o que garantirá que o formset não carregue instâncias existentes.
        return super().get_formset(request, obj, **kwargs)

# Classe do formulário de leilão com calendário
class AuctionAdminForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = '__all__'
    date_time = forms.DateTimeField(widget=AdminDateWidget(attrs={'type': 'datetime-local'}))

class AuctionAdmin(admin.ModelAdmin):
    form = AuctionAdminForm
    list_display = ['codigo_leilao', 'descricao', 'comitente', 'date_time', 'quantidade_lotes', 'status', 'imagem_thumbnail']
    search_fields = ['codigo_leilao', 'descricao', 'comitente']
    list_filter = ['status']
    readonly_fields = ['codigo_leilao']

    fieldsets = (
        ('Status atual do leilão', {
            'fields': ('codigo_leilao', 'status')
        }),
        ('Detalhes do Leilão', {
            'fields': ('descricao', 'categoria', 'comitente', 'complemento')
        }),
        ('Data e Duração', {
            'fields': ('date_time', 'duration_hours', 'quantidade_lotes'),
        }),
        ('Imagem e Documentos', {
            'fields': ('thumbnail', 'documento_editais'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['codigo_leilao']
        return self.readonly_fields
    
    def imagem_thumbnail(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="50" height="50" />', obj.thumbnail.url)
        return "Sem Imagem"

# Base admin para os itens, como veículos, imóveis, etc.
class BaseItemAdmin(admin.ModelAdmin):
    readonly_fields = ['codigo_item', 'valor_arrematado', 'status_pagamento', 'status_lote', 'valor_inicial']
    search_fields = ['codigo_item', 'nome']
    list_display = ['codigo_item', 'nome', 'valor_avaliado_formatado', 'valor_inicial_formatado', 'status_pagamento', 'imagem_thumbnail']
    
    fieldsets = (
        ('Status do item', {
            'fields': ('codigo_item', 'valor_arrematado', 'status_pagamento', 'status_lote'),
        }),
        ('Detalhes do Item', {
            'fields': ('nome', 'descricao','leilao' ,'tipo_item', 'thumbnail', 'destacado')
        }),
        ('Valores', {
            'fields': ('valor_avaliado', 'valor_inicial')
        }),
    )

    def imagem_thumbnail(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="50" height="50" />', obj.thumbnail.url)
        return "Sem Imagem"

    imagem_thumbnail.short_description = 'Imagem'

    def valor_avaliado_formatado(self, obj):
        return locale.currency(obj.valor_avaliado, grouping=True)

    def valor_inicial_formatado(self, obj):
        return locale.currency(obj.valor_inicial, grouping=True)

    valor_avaliado_formatado.short_description = 'Valor Avaliado'
    valor_inicial_formatado.short_description = 'Valor Inicial'

class VehicleAdmin(BaseItemAdmin):
    inlines = [ItemImageInline]  # Aqui adicionamos o Inline de Imagens ao admin do Veículo
    list_display = BaseItemAdmin.list_display
    fieldsets = BaseItemAdmin.fieldsets + (
        ('Detalhes do Veículo', {
            'fields': ('marca', 'modelo', 'fabricacao', 'versao', 'categoria_veiculo', 'fipe')
        }),
        ('Documentação e Condição', {
            'fields': ('tipo_documento', 'tipo_monta', 'tipo_chassi', 'blindado', 'condicao', 'numero_chassi', 'chave', 'final_placa', 'combustivel', 'patio')
        }),
    )

    def fipe_formatado(self, obj):
        return locale.currency(obj.fipe, grouping=True)

    fipe_formatado.short_description = 'Fipe'


class RealEstateAdmin(BaseItemAdmin):
    inlines = [ItemImageInline]  # Adicionamos o Inline aqui também
    list_display = BaseItemAdmin.list_display
    fieldsets = BaseItemAdmin.fieldsets + (
        ('Detalhes do Imóvel', {
            'fields': ('quartos', 'metragem', 'localizacao', 'estado_imovel')
        }),
    )

class RuralItemAdmin(BaseItemAdmin):
    inlines = [ItemImageInline]  # Adicionamos o Inline aqui também
    list_display = BaseItemAdmin.list_display
    fieldsets = BaseItemAdmin.fieldsets + (
        ('Detalhes do Item Rural', {
            'fields': ('origem',)
        }),
    )


class OtherGoodsAdmin(BaseItemAdmin):
    inlines = [ItemImageInline]  # Adicionamos o Inline aqui também
    list_display = BaseItemAdmin.list_display
    fieldsets = BaseItemAdmin.fieldsets

# Registrar os modelos no admin
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(RealEstate, RealEstateAdmin)
admin.site.register(RuralItem, RuralItemAdmin)
admin.site.register(OtherGoods, OtherGoodsAdmin)


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

    fieldsets = (
        (None, {
            'fields': ('nome',)
        }),
    )

# Registrar o modelo ItemImage no admin
class ItemImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'imagem', 'get_image_preview')
    search_fields = ('descricao',)
    list_filter = ('descricao',)
    
    def get_image_preview(self, obj):
        return f'<img src="{obj.imagem.url}" width="100" />'

    get_image_preview.allow_tags = True
    get_image_preview.short_description = 'Pré-visualização da Imagem'

    fields = ('imagem', 'descricao')
    ordering = ('descricao',)

admin.site.register(ItemImage, ItemImageAdmin)
