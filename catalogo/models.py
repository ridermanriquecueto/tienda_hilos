from django.db import models

from django.contrib.auth.models import User

from django.core.exceptions import ValidationError





class Categoria(models.Model):

    nombre = models.CharField(max_length=100, unique=True)

    descripcion = models.TextField(blank=True, null=True)


    class Meta:

        verbose_name = "Categoría"

        verbose_name_plural = "Categorías"


    def __str__(self):

        return self.nombre






class Producto(models.Model):


    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')

    nombre = models.CharField(max_length=100)

    descripcion = models.TextField(default="Descripción predeterminada")

    precio = models.DecimalField(max_digits=10, decimal_places=2)

    imagen = models.ImageField(upload_to='productos/', default='productos/imagen_predeterminada.jpg')

    stock = models.PositiveIntegerField()

    destacado = models.BooleanField(default=False, verbose_name='Destacado')
    oferta = models.BooleanField(default=False, verbose_name='Oferta')


    def clean(self):

        if self.stock is not None and self.stock < 0:

            raise ValidationError('El stock no puede ser negativo.')


    def save(self, *args, **kwargs):

        self.full_clean()

        super(Producto, self).save(*args, **kwargs)


    def __str__(self):

        return self.nombre






class Carrito(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    productos = models.ManyToManyField('Producto', through='ItemCarrito')

    activo = models.BooleanField(default=True)


    class Meta:

        verbose_name = "Carrito"

        verbose_name_plural = "Carritos"


    @property

    def total(self):


        return sum(item.subtotal for item in self.itemcarrito_set.all())


    def __str__(self):

        return f"Carrito de {self.usuario.username} - Activo: {self.activo}"



class ItemCarrito(models.Model):

    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    cantidad = models.PositiveIntegerField(default=1)


    @property

    def subtotal(self):

        return self.producto.precio * self.cantidad


    def clean(self):

        if self.cantidad > self.producto.stock:

            raise ValidationError(f"No hay suficiente stock para {self.producto.nombre}. Disponible: {self.producto.stock}")


    def save(self, *args, **kwargs):

        self.full_clean()

        super(ItemCarrito, self).save(*args, **kwargs)


    def __str__(self):

        return f"{self.producto.nombre} - {self.cantidad} unidades"






class Pedido(models.Model):

    METODOS_PAGO = [

        ('mercado_pago', 'Mercado Pago'),

        ('transferencia', 'Transferencia Bancaria'),

        ('tarjeta', 'Tarjeta de Crédito')

    ]


    ESTADOS_PEDIDO = [

        ('pendiente', 'Pendiente'),

        ('completada', 'Completada'),

        ('cancelada', 'Cancelada')

    ]


    METODOS_ENVIO = [

        ('domicilio', 'Domicilio'),

        ('recoger_tienda', 'Retirar en tienda'),

        ('didi_moto', 'Envío con moto (Didi)'),

        ('uber_moto', 'Envío con moto (Uber)'),

        ('didi_auto', 'Envío con auto (Didi)'),

        ('uber_auto', 'Envío con auto (Uber)'),

        ('agencia', 'Envío por Agencia')

    ]


    TIPOS_VENTA = [

        ('minorista', 'Minorista'),

        ('mayorista', 'Mayorista')

    ]


    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    total = models.DecimalField(max_digits=10, decimal_places=2)

    metodo_pago = models.CharField(max_length=50, choices=METODOS_PAGO)

    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='pendiente')



    nombre_contacto = models.CharField(max_length=100, default='Pedido sin nombre')

    direccion = models.CharField(max_length=255, default='No disponible')

    telefono = models.CharField(max_length=20, default='000000000')

    metodo_envio = models.CharField(max_length=50, choices=METODOS_ENVIO, default='domicilio')

    tipo_venta = models.CharField(max_length=50, choices=TIPOS_VENTA, default='minorista')


    class Meta:

        verbose_name = "Pedido"

        verbose_name_plural = "Pedidos"


    def __str__(self):

        return f"Pedido {self.id} - {self.usuario.username} - Total: ${self.total}"



class LineaPedido(models.Model):

    """
    Guarda el histórico exacto de la venta. 
    Aunque borres el producto de la tienda o cambie su precio, el pedido viejo no se rompe.
    """

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="lineas")

    producto_nombre = models.CharField(max_length=255)

    cantidad = models.PositiveIntegerField()

    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)


    @property

    def total_linea(self):

        return self.precio_unitario * self.cantidad


    def __str__(self):

        return f"{self.producto_nombre} x {self.cantidad}"


class ProductoCambio(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='cambios')
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accion} - {self.producto.nombre} by {self.usuario.username if self.usuario else 'anon'} @ {self.fecha}"
