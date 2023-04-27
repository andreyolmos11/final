from django.contrib import admin
from .models import Direccion, Categoria, Producto, Carrito, Orden

# Register your models here.

class DireccionAdmin(admin.ModelAdmin):
    list_display = ('User', 'localidad', 'municipio', 'departamento')
    list_filter = ('municipio', 'departamento')
    list_per_page = 12
    search_fields = ('localidad', 'municipio', 'departamento')


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'imagen_categoria', 'activo', 'destacado', 'actualizacion')
    list_editable = ('slug', 'activo', 'destacado')
    list_filter = ('activo', 'destacado')
    list_per_page = 12
    search_fields = ('titulo', 'descripcion')
    prepopulated_fields = {'slug': ('titulo',)}


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'categoria', 'imagen_producto', 'activo', 'destacado', 'actualizacion')
    list_editable = ('slug', 'categoria', 'activo', 'destacado')
    list_filter = ('categoria', 'activo', 'destacado')
    list_per_page = 30
    search_fields = ('user', 'producto', 'descripcion_corta')
    prepopulated_fields = {"slug": ("titulo",)}


class CarritoAdmin(admin.ModelAdmin):
    list_display = ('user', 'producto', 'cantidad', 'creacion')
    list_editable = ('cantidad',)
    list_filter = ('creacion',)
    list_per_page = 20
    search_fields = ('usuario', 'producto')


class OrdenAdmin(admin.ModelAdmin):
    list_display = ('user', 'producto', 'cantidad', 'estado', 'fecha_pedido')
    list_editable = ('cantidad', 'estado')
    list_filter = ('estado', 'fecha_pedido')
    list_per_page = 20
    search_fields = ('user', 'producto')


#REGISTRO DE LOS MODELOS EN EL PANEL DE ADMINISTRACION DE DJANGO

admin.site.register(Direccion, DireccionAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(Orden, OrdenAdmin)

