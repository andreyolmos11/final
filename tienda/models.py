from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Direccion(models.Model):
    User = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.CASCADE)
    localidad = models.CharField(max_length=150, verbose_name="Ubicación más cercana")
    municipio = models.CharField(max_length=150, verbose_name="Municipio")
    departamento =models.CharField(max_length=150, verbose_name="Departamento")

    
    def __str__(self):
        return self.localidad


#CLASE CATEGORIA
class Categoria(models.Model):
    titulo = models.CharField(max_length=150, verbose_name="Nombre de la categoria")
    slug = models.SlugField(max_length=55, verbose_name="Identificador de la categoria")
    descripcion = models.TextField(blank=True, verbose_name="Descripcion de la categoria")
    imagen_categoria = models.ImageField(upload_to='categoria', blank=True, null=True, verbose_name="imagen de la categoria")
    activo = models.BooleanField(verbose_name="¿Está activo?")
    destacado = models.BooleanField(verbose_name="¿Está destacado?")
    creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    class Meta:
        verbose_name_plural= 'categorias'
        ordering = ('-creacion',)

    def __str__(self):
        return self.titulo
    

#CLASE PRODUCTO
class Producto(models.Model):
    titulo = models.CharField(max_length=150, verbose_name="Nombre del Producto")
    slug = models.SlugField(max_length=150, verbose_name="Identificador del Producto")
    sku = models.CharField(max_length=250, verbose_name="Identificador unico del producto")
    descripcion_corta = models.TextField(verbose_name="Descripcion Corta del Producto")
    descripcion_detallada = models.TextField(verbose_name="Descripcion Detallada del producto")
    imagen_producto = models.ImageField(upload_to='producto', blank=True, null=True, verbose_name="Imagen Producto")
    precio = models.DecimalField(max_digits=10,decimal_places=6)
    categoria = models.ForeignKey(Categoria, verbose_name="Categoria del Producto", on_delete=models.CASCADE)
    activo = models.BooleanField(verbose_name="¿Está Activo?")
    destacado = models.BooleanField(verbose_name="¿Está destacado?")
    creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")


    class Meta:
        verbose_name_plural= 'productos'
        ordering = ('-creacion', )

    def __str__(self):
        return self.titulo
    

#CLASE CARRITO
class Carrito(models.Model):
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, verbose_name="Producto", on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField(default=1,verbose_name="cantidad")
    creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")


    def __str__(self):
        return str(self.user)
    
# calculo del valor total de los productos añadidos al carrito
    @property
    def precio_total(self):
        return self.cantidad * self.producto.precio
    
#OPCIONES PARA EL ESTADO DEL PEDIDO
ESTADOS_CHOICES = (
    ('Pendiente', 'Pendiente'),
    ('Aceptado', 'Aceptado'),
    ('Empaquetado', 'Empaquetado'),
    ('En Camino', 'En Camino'),
    ('Entregado', 'Entregado'),
    ('Cancelado', 'Cancelado')
)

#CLASE ORDEN
class Orden(models.Model):
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.CASCADE)
    direccion = models.ForeignKey(Direccion, verbose_name="Dirección de envio", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, verbose_name="Producto", on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    fecha_pedido = models.DateTimeField(auto_now_add=True, verbose_name= "Fecha del Pedido")
    estado = models.CharField(
        choices=ESTADOS_CHOICES,
        max_length=50,
        default="pending"
    )