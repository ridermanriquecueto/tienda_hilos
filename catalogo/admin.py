from django.contrib import admin
from .models import Producto
admin.site.register(Producto)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio', 'stock')  # Mostramos más campos en la lista
    search_fields = ('nombre', 'descripcion')  # Permitimos buscar por nombre y descripción
    list_filter = ('precio', 'stock')  # Filtros para precio y stock en la vista de lista
