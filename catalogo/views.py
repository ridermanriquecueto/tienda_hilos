import csv
import pprint
import json
from io import BytesIO
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views import View
from django.views.generic import UpdateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import models 

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

import mercadopago

from .models import Pedido, Producto, Carrito, ItemCarrito, Orden
from .forms import ProductoForm, CheckoutForm
from .boleta import generar_boleta




def alguna_funcion():
    from .views import CarritoView

class OrdenView(models.Model):
    carrito = models.OneToOneField(Carrito, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrdenView {self.id} - Total: ${self.total}"



def inicio(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo/inicio.html')

def productos(request):
    return render(request, 'catalogo/productos.html')

def contacto(request):
    return render(request, 'catalogo/contacto.html')



def procesar_contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono', '')
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        codigo_postal = request.POST.get('codigo_postal')
        comentarios = request.POST.get('comentarios', '')
        metodo_pago = request.POST.get('metodo_pago')

        mensaje = f"""
        Nombre: {nombre}
        Correo: {email}
        Teléfono: {telefono}
        Dirección: {direccion}, {ciudad}, {codigo_postal}
        Método de Pago: {metodo_pago}
        Comentarios: {comentarios}
        """

        send_mail(
            'Nuevo contacto desde la tienda',
            mensaje,
            'tienda@example.com',
            [email],
            fail_silently=False,
        )

        return HttpResponse("Formulario procesado exitosamente.")
    
    return render(request, 'catalogo/contacto.html')

def procesar_envio(request):
    if request.method == 'POST':
        request.session['envio'] = request.POST['envio']
        return redirect('procesar_pago')



def finalizar_compra(request):
    # Obtener el carrito del usuario
    carrito = Carrito.objects.filter(usuario=request.user).first()

    if carrito and carrito.itemcarrito_set.exists():  # Verifica que el carrito tenga ítems
        return redirect('checkout')  # Redirige a la vista del checkout
    else:
        messages.error(request, 'No hay productos en tu carrito.')  # Mensaje de error
        return redirect('carrito')  # Redirigir a la página del carrito si está vacío
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    
    return render(request, 'catalogo/crear_producto.html', {'form': form})

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado exitosamente.')
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    
    return render(request, 'productos/agregar_producto.html', {'form': form})


class ActualizarProductoView(UpdateView):
    model = Producto
    template_name = 'catalogo/actualizar_producto.html'
    fields = ['nombre', 'precio', 'descripcion']
    success_url = '/productos/'



def mi_vista(request):
    productos = Producto.objects.all()
    return render(request, 'mi_template.html', {'productos': productos})

class EliminarProductoView(View):
    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        producto.delete()
        return redirect('listar_productos')  # Redirige después de eliminar
    

def carga_masiva(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')

        if not csv_file or not csv_file.name.endswith('.csv'):
            messages.error(request, 'Por favor, sube un archivo CSV válido.')
            return redirect('productos:carga_masiva')  # Asegúrate de que la URL de carga masiva esté definida

        try:
            # Leer el archivo CSV
            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())

            for row in reader:
                # Validar que los campos necesarios existen
                if not all(field in row for field in ['nombre', 'descripcion', 'precio', 'stock']):
                    messages.error(request, 'El archivo CSV está incompleto.')
                    return redirect('productos:carga_masiva')

                # Intentar convertir precio y stock a tipos adecuados
                try:
                    precio = float(row['precio'])
                    stock = int(row['stock'])
                except ValueError:
                    messages.error(request, 'El precio o el stock tienen un formato incorrecto.')
                    return redirect('productos:carga_masiva')

                # Crear el producto
                Producto.objects.create(
                    nombre=row['nombre'],
                    descripcion=row['descripcion'],
                    precio=precio,
                    stock=stock
                )

            messages.success(request, 'Productos cargados correctamente.')
            return redirect('productos:listar_productos')  # Asegúrate de que esta URL esté definida en tu archivo urls.py

        except Exception as e:
            messages.error(request, f'Hubo un error al procesar el archivo: {e}')
            return redirect('productos:carga_masiva')  # Regresar a la carga masiva si hay un error

    return render(request, 'productos/carga_masiva.html')  # Asegúrate de que la plantilla exista





# Vista para mostrar los detalles de un producto

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'catalogo/detalle_producto.html', {'producto': producto})



def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/listar_productos.html', {'productos': productos})

def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Producto {producto.nombre} actualizado exitosamente.')
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'catalogo/actualizar_producto.html', {'form': form})
    
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, f'El producto {producto.nombre} ha sido eliminado con éxito.')
        return redirect('listar_productos')  # O la vista a la que quieras redirigir
    return render(request, 'catalogo/eliminar_producto.html', {'producto': producto})


def actualizar_item_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, pk=item_id)
    
    nueva_cantidad = request.POST.get('cantidad')
    if nueva_cantidad.isdigit() and int(nueva_cantidad) > 0:
        nueva_cantidad = int(nueva_cantidad)
        
        if nueva_cantidad <= item.producto.stock:
            item.cantidad = nueva_cantidad
            item.save()
            messages.success(request, "Cantidad actualizada correctamente.")
        else:
            messages.error(request, "No hay suficiente stock disponible.")
    else:
        messages.error(request, "Cantidad inválida.")

    return redirect('carrito')

def carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    total = 0
    total_productos = 0  # Variable para contar el número total de productos
    productos_a_eliminar = []

    for producto_id, datos in carrito.items():
        try:
            producto = Producto.objects.get(id=producto_id)
            if producto.precio is None:
                productos_a_eliminar.append(producto_id)
                continue
        except Producto.DoesNotExist:
            productos_a_eliminar.append(producto_id)
            continue

        subtotal = datos['cantidad'] * producto.precio
        items.append({
            'producto': producto,
            'cantidad': datos['cantidad'],
            'subtotal': subtotal,
        })
        total += subtotal
        total_productos += datos['cantidad']  # Sumar la cantidad de cada producto al total

    # Eliminar productos inválidos
    for producto_id in productos_a_eliminar:
        del carrito[producto_id]

    request.session['carrito'] = carrito  # Actualizar el carrito en la sesión
    request.session.modified = True  # Forzar la actualización

    # Pasar la variable total_productos a la plantilla
    return render(request, 'catalogo/carrito.html', {
        'items': items,
        'total': total,
        'total_productos': total_productos,  # Asegúrate de pasar total_productos
    })




def buscar(request):
    query = request.GET.get('q')
    resultados = Producto.objects.filter(nombre__icontains=query) if query else []
    return render(request, 'catalogo/buscar.html', {'resultados': resultados, 'query': query})



def actualizar_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        cantidad = int(request.POST.get('cantidad', 1))  # Obtiene la cantidad del formulario
        if cantidad > 0:
            carrito[str(producto_id)]['cantidad'] = cantidad  # Actualiza la cantidad
        else:
            del carrito[str(producto_id)]  # Elimina el producto si la cantidad es 0

    request.session['carrito'] = carrito
    return redirect('ver_carrito')  # Redirige a la vista del carrito


def eliminar_del_carrito(request, producto_id, eliminar_todo=0):
    # Convertir eliminar_todo de entero a booleano
    eliminar_todo = bool(int(eliminar_todo))  # Convertimos el valor a entero y luego a booleano

    # Obtener el carrito del usuario
    carrito = Carrito.objects.get(usuario=request.user)  # Aquí cambiamos user por usuario

    # Verificar si el producto existe en el carrito
    if producto_id in carrito.productos:
        if eliminar_todo:
            # Eliminar el producto completo del carrito
            carrito.productos.remove(producto_id)
        else:
            # Reducir la cantidad en 1 si hay más de 1 producto
            producto = carrito.productos.get(id=producto_id)
            if producto.cantidad > 1:
                producto.cantidad -= 1
            else:
                # Si la cantidad es 1, eliminar el producto del carrito
                carrito.productos.remove(producto)

        # Guardar el carrito actualizado
        carrito.save()

    # Redirigir al carrito para mostrar los cambios
    return redirect('ver_carrito')

def procesar_carrito(request, nombre, direccion, telefono, metodo_pago, metodo_envio):
    carrito = obtener_carrito(request.session)

    if not carrito:
        messages.error(request, "El carrito está vacío.")
        return redirect('productos:carrito')

    return guardar_pedido(request, carrito, nombre, direccion, telefono, metodo_pago, metodo_envio)


def finalizar_compra(request):
    if request.method == 'POST':
        # Obtener el carrito de la sesión
        carrito = request.session.get('carrito', {})

        try:
            # Calcular el total, asegurándose de convertir los valores a float
            total = sum(float(item['precio']) * int(item['cantidad']) for item in carrito.values())

            # Simulación de procesamiento de pago (por ejemplo)
            pago_exitoso = True  # Esto debería ser el resultado de la lógica de pago real

            if pago_exitoso:
                # Limpia el carrito después de la compra
                request.session['carrito'] = {}

                # Agregar un mensaje de éxito
                messages.success(request, "Compra finalizada con éxito. Gracias por tu compra!")

                # Redirigir a la página de compra exitosa
                return redirect('compra_exitosa')
            else:
                messages.error(request, "Hubo un problema al finalizar la compra. Inténtalo nuevamente.")
        except (ValueError, TypeError):
            messages.error(request, "Los datos del carrito no son válidos para calcular el total.")

    # Redirigir de vuelta a la vista del carrito si no es un POST
    return redirect('ver_carrito')


def procesar_pago(request):
    if request.method == 'POST':
        # Aquí agregarías la lógica para procesar el pago.
        # Por ejemplo, podrías integrar un API de un proveedor de pagos (Stripe, PayPal, etc.)
        
        # Simulación de procesamiento de pago
        pago_exitoso = True  # Cambia esto según el resultado real del pago.

        if pago_exitoso:
            # Aquí podrías guardar el pedido en la base de datos si es necesario
            # e.g. Pedido.objects.create(...)

            # Limpia el carrito después de un pago exitoso
            request.session['carrito'] = {}

            # Agregar un mensaje de éxito
            messages.success(request, "Gracias por tu compra! Tu pedido ha sido procesado.")

            # Redirigir a la página de compra exitosa
            return redirect('compra_exitosa')  # Cambia 'compra_exitosa' al nombre de tu URL correspondiente.
        else:
            messages.error(request, "Hubo un error al procesar tu pago. Inténtalo de nuevo.")

    return render(request, 'carrito/checkout.html')  # Devuelve la página de checkout si no es un POST.


def politicas_envio(request):
    return render(request, 'catalogo/politicas_envio.html')
def agregar_al_carrito(request, producto_id):
    # Obtener el producto de la base de datos o devolver un error 404 si no existe
    producto = get_object_or_404(Producto, id=producto_id)

    # Asegurarse de que el precio del producto no sea nulo
    if producto.precio is None:
        print(f"Producto {producto_id} no tiene precio asignado!")
        return redirect('ver_carrito')

    # Obtener el carrito de la sesión, si no existe, crear uno vacío
    carrito = request.session.get('carrito', {})

    # Obtener la cantidad seleccionada desde el formulario (valor por defecto 1) y validación
    cantidad = request.POST.get('cantidad', 1)
    try:
        cantidad = max(1, int(cantidad))  # Asegura que la cantidad sea al menos 1
    except ValueError:
        cantidad = 1  # Si no es un número válido, asignamos 1 como valor predeterminado

    # Calcular el subtotal (producto.precio debería ser un valor numérico)
    precio = producto.precio if producto.precio is not None else 0.0
    print(f"Producto {producto_id} - Precio: {precio} - Cantidad: {cantidad} - Subtotal: {precio * cantidad}")

    subtotal = precio * cantidad

    # Agregar o actualizar el producto en el carrito
    producto_id_str = str(producto_id)
    if producto_id_str in carrito:
        # Si el producto ya está en el carrito, actualizar la cantidad y el subtotal
        carrito[producto_id_str]['cantidad'] += cantidad
        carrito[producto_id_str]['subtotal'] = carrito[producto_id_str]['precio'] * carrito[producto_id_str]['cantidad']
    else:
        # Si el producto no está en el carrito, agregarlo
        carrito[producto_id_str] = {
            'nombre': producto.nombre,
            'precio': precio,  # Asegurarse de que el precio sea un número flotante
            'cantidad': cantidad,
            'subtotal': subtotal
        }

    # Guardar el carrito actualizado en la sesión
    request.session['carrito'] = carrito

    # Redirigir al carrito
    return redirect('ver_carrito')  # Asegúrate de que 'ver_carrito' esté en tus URLs

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    total = 0
    total_productos = 0  # Variable para contar el número total de productos

    # Hacemos una copia del carrito para evitar modificar el diccionario mientras se itera
    carrito_copy = carrito.copy()

    for producto_id, datos in carrito_copy.items():
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            # Si el producto no existe, eliminarlo del carrito original
            del carrito[producto_id]
            continue  # Saltar a la siguiente iteración

        # Verificar que la cantidad en el carrito no exceda el stock disponible
        if datos['cantidad'] > producto.stock:
            # Si la cantidad solicitada excede el stock, ajustamos la cantidad en el carrito
            datos['cantidad'] = producto.stock
            carrito[producto_id]['cantidad'] = producto.stock  # Actualizamos el carrito en la sesión
            # Informar al usuario de la corrección
            mensaje = f"La cantidad del producto '{producto.nombre}' ha sido ajustada al stock disponible ({producto.stock})."
            request.session['mensaje_stock'] = mensaje
        
        subtotal = datos['cantidad'] * producto.precio
        items.append({
            'producto': producto,
            'cantidad': datos['cantidad'],
            'subtotal': subtotal,
        })
        total += subtotal
        total_productos += datos['cantidad']  # Sumar la cantidad de cada producto al total

    # Guardar el carrito actualizado en la sesión
    request.session['carrito'] = carrito

    # Obtener el mensaje de stock si existe
    mensaje_stock = request.session.pop('mensaje_stock', None)

    return render(request, 'catalogo/carrito.html', {
        'items': items,
        'total': total,
        'total_productos': total_productos,
        'mensaje_stock': mensaje_stock  # Para mostrar el mensaje al usuario si hubo un ajuste
    })


def catalogo(request):
    query = request.GET.get('search', '')  # Obtener la búsqueda del formulario
    if query:
        # Filtrar productos por el nombre que contiene el texto de búsqueda
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        # Si no hay búsqueda, mostrar todos los productos
        productos = Producto.objects.all()

    # Configuración de paginación
    paginator = Paginator(productos, 10)  # Mostrar 10 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Renderizar la plantilla con los productos filtrados o todos
    return render(request, 'catalogo.html', {'productos': page_obj})
# Vista para el catálogo de productos


def catalogo_listar(request):
    search_query = request.GET.get('search', '')  # Obtén la búsqueda desde el formulario
    if search_query:
        productos = Producto.objects.filter(nombre__icontains=search_query)  # Filtrar por nombre
    else:
        productos = Producto.objects.all()  # Si no hay búsqueda, mostrar todos
    return render(request, 'catalogo/catalogo_listar.html', {'productos': productos})





class OrdenView(models.Model):
    carrito = models.OneToOneField(Carrito, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrdenView {self.id} - Total: ${self.total}"
    
def vista_orden(request):
    carrito_id = request.session.get('carrito_id')
    carrito = Carrito.objects.get(id=carrito_id) if carrito_id else None
    
    if request.method == 'POST':
        # Crear la orden
        nombre_cliente = request.POST['nombre']
        email_cliente = request.POST['email']
        direccion_cliente = request.POST['direccion']
        
        orden = Orden.objects.create(carrito=carrito, nombre_cliente=nombre_cliente, 
                            email_cliente=email_cliente, direccion_cliente=direccion_cliente)
        # Redirigir a la página de confirmación o a otra parte
        return redirect('confirmacion_orden', orden_id=orden.id)
    
    return render(request, 'vista_orden.html', {'carrito': carrito})

class CarritoView(View):
    def get(self, request):
        # Obtener el carrito desde la sesión
        carrito = request.session.get('carrito', {})
        
        # Calcular el total sumando precio * cantidad para cada ítem
        total = sum(float(item['precio']) * int(item['cantidad']) for item in carrito.values())
        
        # Pasar los datos a la plantilla
        return render(request, 'catalogo/carrito.html', {
            'carrito': carrito,
            'total': total
        })




def some_function():
    from .views import CarritoView  # Importación dentro de la función
    # Lógica que usa CarritoView

def catalogo_view(request):
    productos = Producto.objects.all()  # Ajusta según tus necesidades
    return render(request, 'catalogo/catalogo.html', {'productos': productos})

def compra_exitosa(request):
    # Lógica para la vista de compra exitosa
    return render(request, 'compra_exitosa.html')  

def checkout(request):
    carrito = request.session.get('carrito', {})

    # DEBUG: Verificar el contenido del carrito antes de cualquier cálculo
    print("Carrito en sesión:", carrito)

    # Validar que todos los productos tengan precio y cantidad válidos antes de calcular el total
    for producto_id, item in carrito.items():
        if item.get('precio') is None or item.get('cantidad') is None:
            print(f"⚠️ Producto con datos incorrectos: {producto_id} -> {item}")
            messages.error(request, f"Error en el carrito: El producto {item.get('nombre', 'desconocido')} tiene datos incorrectos.")
            return redirect('carrito')

    try:
        totalCarrito = sum(Decimal(item['precio']) * item['cantidad'] for item in carrito.values())
    except Exception as e:
        print("❌ Error calculando total del carrito:", e)
        messages.error(request, "Error en el carrito: falta información de precios.")
        return redirect('carrito')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        metodo_pago = request.POST.get('metodo_pago')
        metodo_envio = request.POST.get('metodo_envio')
        numero_tarjeta = request.POST.get('numero_tarjeta', '')

        # Alias predeterminado para Mercado Pago
        alias_mercado_pago = request.POST.get('alias_mercado_pago', 'rider.hilos')

        # Validar que los campos requeridos no estén vacíos
        if not nombre or not direccion or not telefono or not metodo_pago or not metodo_envio:
            messages.error(request, "Por favor, complete todos los campos obligatorios.")
            return redirect('checkout')

        # Políticas de Envío
        if metodo_envio == 'domicilio':
            costo_envio = 10 if totalCarrito < 50000 else 0
        else:  # método 'recoger_tienda'
            costo_envio = 0

        totalConEnvio = totalCarrito + costo_envio

        # Procesar el pago según el método
        if metodo_pago == 'mercado_pago':
            messages.success(request, "Será redirigido a Mercado Pago para completar su pago.")
            return redirect('mercado_pago')  # Suponiendo que tienes una vista para esto

        if metodo_pago in ['cuenta_dni', 'efectivo', 'transferencia_bancaria', 'tarjeta_credito']:
            if metodo_pago == 'tarjeta_credito' and not numero_tarjeta:
                messages.error(request, "Debe ingresar el número de tarjeta.")
                return redirect('checkout')

            messages.success(request, f"Pago con {metodo_pago.capitalize()} confirmado. Total: ${totalConEnvio}.")

            # Verificar que todos los parámetros sean válidos antes de generar la boleta
            if not nombre or not totalConEnvio or not carrito or not metodo_pago or not alias_mercado_pago:
                messages.error(request, "Faltan datos para generar la boleta.")
                return redirect('checkout')

            # Convertir el carrito a una cadena JSON
            productos_str = json.dumps(carrito)

            # Verificar que totalConEnvio es un número válido
            if not isinstance(totalConEnvio, (int, float, Decimal)):
                messages.error(request, "El total es inválido.")
                return redirect('checkout')

            # Generar la URL para la boleta
            try:
                url = reverse('generar_boleta', kwargs={
                    'nombre': nombre,
                    'total': totalConEnvio,  
                    'productos': productos_str,  
                    'metodo_pago': metodo_pago,
                    'alias': alias_mercado_pago
                })
            except Exception as e:
                messages.error(request, f"Error al generar la URL: {e}")
                return redirect('checkout')

            return redirect(url)

    return render(request, 'productos/checkout.html', {'totalCarrito': totalCarrito, 'carrito': carrito})






def procesar_envio(request):
    if request.method == "POST":
        distancia = float(request.POST.get('distancia'))
        metodo_envio = request.POST.get('envio')
        costo_envio = 0

        # Calcular el costo de envío según la distancia
        if metodo_envio == "moto" and distancia <= 20:
            costo_envio = 0  # Envío gratuito o costo mínimo dependiendo del servicio (Didi, Uber, etc.)
        elif metodo_envio == "agencia" and distancia > 50:
            costo_envio = "A consultar según la agencia"  # Este costo varía por agencia
        elif metodo_envio == "moto" and distancia > 20:
            costo_envio = 50  # Envío por Uber/Didi/Moto para distancias mayores a 20 km

        # Guardar la información en la sesión o base de datos
        request.session['metodo_envio'] = metodo_envio
        request.session['distancia'] = distancia
        request.session['costo_envio'] = costo_envio

        # Redirigir a una página de confirmación o finalización
        return redirect('confirmar_envio')  # Cambia esto al nombre de tu vista de confirmación

    return HttpResponse("Método no permitido", status=405)


   

def mostrar_carrito(request):
    carrito = request.session.get('carrito', {})
    
    for item in carrito.values():
        item['total'] = item['producto'].precio * item['cantidad']

    total_general = sum(item['total'] for item in carrito.values())

    context = {
        'carrito': carrito,
        'total': total_general
    }

    return render(request, 'catalogo/checkout.html', context)


def procesar_compra(request):
    if request.method == 'POST':
        # Validar que todos los campos necesarios estén presentes
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        metodo_pago = request.POST.get('metodo_pago')
        metodo_envio = request.POST.get('metodo_envio')

        if not all([nombre, direccion, telefono, metodo_pago, metodo_envio]):
            messages.error(request, "Por favor, complete todos los campos obligatorios.")
            return redirect('productos:finalizar_compra')

        # Continuar al siguiente paso si los datos son válidos
        return procesar_carrito(request, nombre, direccion, telefono, metodo_pago, metodo_envio)

    return redirect('productos:carrito')

from .models import Orden, ProductoOrden
from .utils import enviar_confirmacion_compra  # Importamos la función
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def confirmar_compra(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        direccion = request.POST.get("direccion")
        telefono = request.POST.get("telefono")
        metodo_pago = request.POST.get("metodo_pago")
        metodo_envio = request.POST.get("metodo_envio")
        
        # Obtener productos del carrito
        carrito = request.session.get("carrito", {})

        if not carrito:
            messages.error(request, "Tu carrito está vacío.")
            return redirect("carrito")

        # 🔍 Depurar: imprimir contenido del carrito en la consola
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(carrito)

        # Verificar que todos los productos tienen la clave "total"
        for item in carrito.values():
            if "total" not in item:
                messages.error(request, "Error en el carrito: falta información de precios.")
                return redirect("carrito")

        # Crear la orden
        nueva_orden = Orden.objects.create(
            usuario=request.user,
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            metodo_pago=metodo_pago,
            metodo_envio=metodo_envio,
            total=sum(item.get("total", 0) for item in carrito.values())  # 🔹 Se usa .get() para evitar KeyError
        )

        # Guardar los productos en la orden
        for item in carrito.values():
            ProductoOrden.objects.create(
                orden=nueva_orden,
                producto_nombre=item.get("nombre", "Producto sin nombre"),
                cantidad=item.get("cantidad", 0),
                precio=item.get("precio", 0),
                total=item.get("total", 0)  # 🔹 Se usa .get() para mayor seguridad
            )

        # 🔹 Enviar correo de confirmación
        enviar_confirmacion_compra(request.user, nueva_orden)

        # Limpiar el carrito
        request.session["carrito"] = {}
        request.session.modified = True  # Asegura que los cambios en la sesión se guarden

        messages.success(request, "¡Tu compra se ha realizado con éxito! Revisa tu correo.")
        return redirect("orden_exitosa")  # Redirigir a una página de confirmación

    return redirect("checkout")

@login_required
def crear_orden(request):
    carrito = Carrito.objects.filter(usuario=request.user, activo=True).first()
    if not carrito:
        messages.error(request, "No tienes un carrito activo.")
        return redirect('home')

    # Calcular el total
    total = sum(item.cantidad * item.producto.precio for item in carrito.itemcarrito_set.all())
    carrito.total = total
    carrito.save()

    # Crear la orden
    orden = Orden.objects.create(
        carrito=carrito,
        total=total,
        metodo_pago=request.POST.get('metodo_pago'),
        metodo_envio=request.POST.get('metodo_envio')
    )

    # Marcar el carrito como no activo
    carrito.activo = False
    carrito.save()

    messages.success(request, f"Tu orden ha sido creada con éxito. El total es ${total}.")
    return redirect('confirmacion_orden', orden_id=orden.id)


def orden_exitosa(request):
    return render(request, "catalogo/orden_exitosa.html")

def confirmacion_orden(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)
    return render(request, 'confirmacion_orden.html', {'orden': orden})

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirigir a la página de inicio después de login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})
