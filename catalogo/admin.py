from django.contrib import admin

from .models import Producto, Categoria


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'destacado', 'oferta')
    list_editable = ('precio', 'stock', 'destacado', 'oferta')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('categoria', 'destacado', 'oferta')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

