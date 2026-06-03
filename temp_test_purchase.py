import os
import sys
from decimal import Decimal

sys.path.insert(0, r'E:\Hilos')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hilos.settings')
import django
django.setup()

from django.test import Client
from catalogo.models import Producto

producto = Producto.objects.first()
if producto is None:
    producto = Producto.objects.create(
        nombre='Prueba Hilo',
        descripcion='Hilo de prueba',
        precio=Decimal('99.90'),
        stock=10
    )

print('Producto inicial:', producto.id, producto.nombre, producto.stock)
client = Client()
resp = client.get('/catalogo/')
print('GET /catalogo/ status', resp.status_code)
resp = client.post(f'/agregar/{producto.id}/', {'cantidad': 2})
print('POST agregar status', resp.status_code, getattr(resp, 'url', ''))
resp = client.get('/carrito/')
print('GET /carrito/ status', resp.status_code)
print('Carrito content length', len(resp.content))
resp = client.post('/confirmar-compra/', {
    'nombre': 'Test Usuario',
    'direccion': 'Calle Falsa 123',
    'telefono': '123456789',
    'metodo_pago': 'tarjeta',
    'metodo_envio': 'domicilio'
})
print('POST confirmar_compra status', resp.status_code, getattr(resp, 'url', ''))
producto.refresh_from_db()
print('Producto final stock:', producto.stock)
