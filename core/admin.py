from django.contrib import admin
from .models import Categoria, Produto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    pass

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'categoria', 'preco')
    list_filter = ('categoria',)
    list_editable = ('preco',)
    search_fields = ('nome', 'descricao')