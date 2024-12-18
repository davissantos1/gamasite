from django.contrib import admin
from .models import Arrematante, Admin, Documento
from django.utils.html import format_html


# Inline para exibição de documentos relacionados
class DocumentoInline(admin.TabularInline):
    model = Documento
    extra = 0
    fields = ('tipo_documento', 'documento_tag', 'data_upload')
    readonly_fields = ('documento_tag', 'data_upload')  # data_upload é somente leitura

    def documento_tag(self, obj):
        if obj.documento:
            return format_html(f'<a href="{obj.documento.url}" target="_blank">Visualizar Documento</a>')
        return "-"
    
    documento_tag.short_description = "Documento"


# Admin para Arrematante
class ArrematanteAdmin(admin.ModelAdmin):
    list_display = ('user', 'cpf_cnpj', 'cidade', 'estado', 'tipo_cadastro', 'telefone_celular')
    search_fields = ('user__username', 'cpf_cnpj', 'cidade')
    list_filter = ('tipo_cadastro', 'estado', 'cidade')
    inlines = [DocumentoInline]  # Adiciona a exibição de documentos no admin do Arrematante

    def get_queryset(self, request):
        # Filtra os Arrematantes com base no tipo de cadastro
        queryset = super().get_queryset(request)
        return queryset

admin.site.register(Arrematante, ArrematanteAdmin)


# Admin para Administradores
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'setor', 'telefone')
    search_fields = ('user__username', 'setor')
    list_filter = ('setor',)

admin.site.register(Admin, AdminAdmin)


# Admin para Documentos
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('tipo_documento', 'documento_tag', 'data_upload', 'get_usuario')
    search_fields = ('tipo_documento', 'arrematante__user__username')
    list_filter = ('tipo_documento', 'data_upload')
    readonly_fields = ('documento_tag', 'data_upload')  # Adicionado data_upload como somente leitura

    def documento_tag(self, obj):
        if obj.documento:
            return format_html(f'<a href="{obj.documento.url}" target="_blank">Visualizar Documento</a>')
        return "-"
    
    documento_tag.short_description = "Documento"

    def get_usuario(self, obj):
        if obj.arrematante:
            return f"Arrematante: {obj.arrematante.user.username}"
        elif obj.vendedor:
            return f"Vendedor: {obj.vendedor.user.username}"
        return "N/A"

    get_usuario.short_description = "Usuário"

    def get_queryset(self, request):
        # Personaliza a exibição de documentos com base no tipo de usuário
        queryset = super().get_queryset(request)
        return queryset

admin.site.register(Documento, DocumentoAdmin)
