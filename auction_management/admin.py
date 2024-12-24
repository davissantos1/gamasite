from django.contrib import admin
from .models import Auction, Vehicle, RealEstate, RuralItem, OtherGoods, ItemImage, ItemType
from django.utils.html import format_html
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
import locale

# Definir a localidade para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class ItemImageAdmin(admin.ModelAdmin):
    # Campos que serão exibidos na lista de itens do admin
    list_display = ('id', 'descricao', 'imagem', 'get_image_preview')
    
    # Campos que serão usados para pesquisa
    search_fields = ('descricao',)
    
    # Filtros para facilitar a busca
    list_filter = ('descricao',)
    
    # Campos de visualização de imagem na administração
    def get_image_preview(self, obj):
        return f'<img src="{obj.imagem.url}" width="100" />'
    
    get_image_preview.allow_tags = True
    get_image_preview.short_description = 'Pré-visualização da Imagem'

    # Configurações de campo para o formulário de edição de itens
    fields = ('imagem', 'descricao')
    # Definir a ordem dos campos no formulário de edição
    ordering = ('descricao',)

# Registrar o modelo e o admin personalizado
admin.site.register(ItemImage, ItemImageAdmin)

# Definir o Inline para Imagens
class VehicleItemImageInline(admin.TabularInline):
    model = Vehicle.imagens.through
    extra = 1
    fields = ['imagem_display', 'itemimage']  # Exibir imagem e link para o campo de imagem
    readonly_fields = ['imagem_display']  # Tornar a exibição da imagem somente leitura
    can_delete = True
    show_change_link = True
    verbose_name = 'Imagem do Item'
    verbose_name_plural = 'Imagens dos Itens'

    # Método para exibir a imagem no admin
    def imagem_display(self, obj):
        if obj.itemimage.imagem:
            return format_html('<img src="{}" width="100" />', obj.itemimage.imagem.url)
        return "Sem Imagem"
    imagem_display.short_description = 'Visualização da Imagem'



# Definir o Inline para Imagens
class RealEstateItemImageInline(admin.TabularInline):
    model = RealEstate.imagens.through
    extra = 0
    fields = ['imagem_display', 'itemimage']  # Exibir imagem e link para o campo de imagem
    readonly_fields = ['imagem_display']  # Tornar a exibição da imagem somente leitura
    can_delete = True
    show_change_link = True
    verbose_name = 'Imagem do Item'
    verbose_name_plural = 'Imagens dos Itens'

    # Método para exibir a imagem no admin
    def imagem_display(self, obj):
        if obj.itemimage:
            return format_html('<img src="{}" width="100" />', obj.itemimage.url)
        return "Sem Imagem"
    imagem_display.short_description = 'Visualização da Imagem'

# Definir o Inline para Imagens
class OtherGoodsItemImageInline(admin.TabularInline):
    model = OtherGoods.imagens.through
    extra = 0
    fields = ['imagem_display', 'itemimage']  # Exibir imagem e link para o campo de imagem
    readonly_fields = ['imagem_display']  # Tornar a exibição da imagem somente leitura
    can_delete = True
    show_change_link = True
    verbose_name = 'Imagem do Item'
    verbose_name_plural = 'Imagens dos Itens'

    # Método para exibir a imagem no admin
    def imagem_display(self, obj):
        if obj.itemimage:
            return format_html('<img src="{}" width="100" />', obj.itemimage.url)
        return "Sem Imagem"
    imagem_display.short_description = 'Visualização da Imagem'

# Definir o Inline para Imagens
class RuralItemItemImageInline(admin.TabularInline):
    model = RuralItem.imagens.through
    extra = 0
    fields = ['imagem_display', 'itemimage']  # Exibir imagem e link para o campo de imagem
    readonly_fields = ['imagem_display']  # Tornar a exibição da imagem somente leitura
    can_delete = True
    show_change_link = True
    verbose_name = 'Imagem do Item'
    verbose_name_plural = 'Imagens dos Itens'

    # Método para exibir a imagem no admin
    def imagem_display(self, obj):
        if obj.itemimage:
            return format_html('<img src="{}" width="100" />', obj.itemimage.url)
        return "Sem Imagem"
    imagem_display.short_description = 'Visualização da Imagem'

# Definir a classe do formulário para adicionar o calendário aos campos de data
class AuctionAdminForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = '__all__'
    date_time = forms.DateTimeField(widget=AdminDateWidget(attrs={'type': 'datetime-local'}))

class AuctionAdmin(admin.ModelAdmin):
    form = AuctionAdminForm
    list_display = ['codigo_leilao', 'descricao', 'comitente', 'date_time', 'quantidade_lotes', 'active']
    search_fields = ['codigo_leilao', 'descricao', 'comitente']
    list_filter = ['active']
    readonly_fields = ['codigo_leilao']

    fieldsets = (
        ('Detalhes do Leilão', {
            'fields': ('codigo_leilao', 'descricao', 'categoria', 'comitente', 'complemento', 'active')
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
            'fields': ( 'valor_avaliado', 'valor_inicial')
        }),
    )

    # Método para exibir a miniatura da imagem na listagem
    def imagem_thumbnail(self, obj):
        # Verifica se o item tem um atributo thumbnail
        if obj.thumbnail:
            return format_html('<img src="{}" width="50" height="50" />', obj.thumbnail.url)
        return "Sem Imagem"

    imagem_thumbnail.short_description = 'Imagem'

    # Métodos para formatar os campos como moeda brasileira (R$)
    def valor_avaliado_formatado(self, obj):
        return locale.currency(obj.valor_avaliado, grouping=True)

    def valor_inicial_formatado(self, obj):
        return locale.currency(obj.valor_inicial, grouping=True)

    def valor_arrematado_formatado(self, obj):
        return locale.currency(obj.valor_arrematado, grouping=True)

    # Definir os nomes para os campos formatados
    valor_avaliado_formatado.short_description = 'Valor Avaliado'
    valor_inicial_formatado.short_description = 'Valor Inicial'
    valor_arrematado_formatado.short_description = 'Valor Arrematado'

class VehicleAdmin(BaseItemAdmin):
    list_display = BaseItemAdmin.list_display
    fieldsets = BaseItemAdmin.fieldsets + (
        ('Detalhes do Veículo', {
            'fields': ('marca', 'modelo', 'fabricacao', 'versao', 'categoria_veiculo', 'fipe')
        }),
        ('Documentação e Condição', {
            'fields': ('tipo_documento', 'tipo_monta', 'tipo_chassi', 'blindado', 'condicao', 'numero_chassi', 'chave', 'final_placa', 'combustivel', 'patio')
        }),
    )

    inlines = [VehicleItemImageInline]

    # Método para formatar o valor de 'fipe' como moeda brasileira
    def fipe_formatado(self, obj):
        return locale.currency(obj.fipe, grouping=True)

    fipe_formatado.short_description = 'Fipe'


class RealEstateAdmin(BaseItemAdmin):
    list_display = BaseItemAdmin.list_display
    fieldsets = BaseItemAdmin.fieldsets + (
        ('Detalhes do Imóvel', {
            'fields': ('quartos', 'metragem', 'localizacao', 'estado_imovel')
        }),
    )

    inlines = [RealEstateItemImageInline]


class RuralItemAdmin(BaseItemAdmin):
    list_display = BaseItemAdmin.list_display
    fieldsets = BaseItemAdmin.fieldsets + (
        ('Detalhes do Item Rural', {
            'fields': ('origem',)
        }),
    )

    inlines = [RuralItemItemImageInline]


class OtherGoodsAdmin(BaseItemAdmin):
    list_display = BaseItemAdmin.list_display
    fieldsets = BaseItemAdmin.fieldsets

    inlines = [OtherGoodsItemImageInline]


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