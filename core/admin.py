from django.contrib import admin
from .models import Categoria, Produto, Divulgacoes, Garcom, Mesa, Informacoes, Pedidos, ItemPedido, Categoria
from django.utils.html import format_html
from .forms import CategoriaForm

class CategoriaAdmin(admin.ModelAdmin):
    form = CategoriaForm

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'ativo', 'thumb')
    list_filter = ('categoria',)
    list_editable = ('preco',)
    search_fields = ('nome', 'descricao')

    def thumb(self, obj):
        if obj.imagem:
            return format_html(f'<img src="{obj.imagem.url}" width="50" height="50" />')
        return "-"
    thumb.short_description = 'Imagem'

@admin.register(Divulgacoes)
class DivulgacoesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo')
    list_filter = ('ativo',)
    fields = ('nome', 'imagem', 'ativo')

@admin.register(Garcom)
class GarcomAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo')
    search_fields = ('nome',)
    list_filter = ('ativo',)

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'garcom', 'taxa', 'ativo')
    list_filter = ('garcom', 'taxa', 'ativo')
    search_fields = ('numero',)

@admin.register(Informacoes)
class InformacoesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo', 'tema')
    search_fields = ('nome',)
    list_filter = ('ativo',)
    fields = ('nome', 'logo', 'sobre', 'ativo', 'tema')

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(f'<img src="{obj.logo.url}" width="60" height="60" style="object-fit:contain;" />')
        return "-"
    logo_preview.short_description = 'Logo'

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    form = CategoriaForm

admin.site.site_header = "TechRest"
admin.site.site_title = "Administração"
admin.site.index_title = "Bem-vindo ao sistema"
