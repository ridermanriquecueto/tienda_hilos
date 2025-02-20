from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(default="Descripción predeterminada")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', default='productos/imagen_predeterminada.jpg')
    stock = models.PositiveIntegerField()

    def clean(self):
        if self.stock < 0:
            raise ValidationError('El stock no puede ser negativo.')

    def __str__(self):
        return self.nombre


class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField('Producto', through='ItemCarrito')
    activo = models.BooleanField(default=True)  # Campo para saber si el carrito está activo
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total calculado

    class Meta:
        verbose_name_plural = "Carritos"

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.cantidad > self.producto.stock:
            raise ValidationError(f"No hay suficiente stock para {self.producto.nombre}.")
        super(ItemCarrito, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades"



    
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    carrito = models.OneToOneField('Carrito', on_delete=models.CASCADE)  # Asume que existe un modelo Carrito
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(
        max_length=50,
        choices=[
            ('mercado_pago', 'Mercado Pago'),
            ('transferencia', 'Transferencia Bancaria'),
            ('tarjeta', 'Tarjeta de Crédito')
        ]
    )
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('completada', 'Completada')
        ],
        default='pendiente'
    )
    nombre = models.CharField(max_length=100, default='Pedido sin nombre')
    direccion = models.CharField(max_length=255, default='No disponible')  # Valor por defecto
    telefono = models.CharField(max_length=20, default='000000000')
    metodo_envio = models.CharField(
        max_length=50,
        choices=[
            ('domicilio', 'Domicilio'),
            ('recoger', 'Recoger en tienda')
        ],
        default='domicilio'
    )
    tipo_venta = models.CharField(max_length=50, default='minorista')

    def __str__(self):
        return f"Pedido {self.id} - Total: ${self.total}"


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirige a la página de inicio o a donde desees
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

class Orden(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    metodo_pago = models.CharField(max_length=50)
    metodo_envio = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden {self.id} - {self.usuario.username}"

class ProductoOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name="productos")
    producto_nombre = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto_nombre} - {self.cantidad} unidades"