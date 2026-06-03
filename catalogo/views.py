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
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from django.core.exceptions import ObjectDoesNotExist

from django.core.paginator import Paginator

from django.db import models 


from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import letter


import mercadopago



from .models import Pedido, LineaPedido, Producto, Carrito, ItemCarrito

from .forms import ProductoForm, CheckoutForm

from .boleta import generar_boleta

from .utils import calcular_costo_envio, get_metodo_envio_display, enviar_confirmacion_compra                           






def alguna_funcion():

    from .views import CarritoView


def custom_login(request):


    return render(request, 'registration/login.html')






def inicio(request):
    # Mostrar destacados (productos marcados) y ofertas (productos marcados como oferta)
    destacados = Producto.objects.filter(destacado=True, stock__gt=0).order_by('-id')[:6]
    ofertas = Producto.objects.filter(oferta=True, stock__gt=0).order_by('precio')[:6]
    carrito = request.session.get('carrito', [])
    return render(request, 'catalogo/inicio.html', {'destacados': destacados, 'ofertas': ofertas, 'carrito': carrito})


def productos(request):

    productos = Producto.objects.all()  

    return render(request, 'catalogo/productos.html', {'productos': productos})


def contacto(request):

    return render(request, 'catalogo/contacto.html')


def buscar(request):

    query = request.GET.get('q')

    resultados = Producto.objects.filter(nombre__icontains=query).order_by('categoria__nombre', 'nombre') if query else Producto.objects.none()

    return render(request, 'catalogo/buscar.html', {'resultados': resultados, 'query': query})


def catalogo(request):

    query = request.GET.get('search', '')  

    if query:

        productos = Producto.objects.filter(nombre__icontains=query).order_by('categoria__nombre', 'nombre')

    else:

        productos = Producto.objects.all().order_by('categoria__nombre', 'nombre')


    paginator = Paginator(productos, 10)  

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request, 'catalogo.html', {'productos': page_obj})


def catalogo_listar(request):

    query = request.GET.get('search', '')
    if query:
        productos = Producto.objects.filter(nombre__icontains=query).order_by('categoria__nombre', 'nombre')
    else:
        productos = Producto.objects.all().order_by('categoria__nombre', 'nombre')

    return render(request, 'catalogo/catalogo_listar.html', {'productos': productos})


def detalle_producto(request, producto_id):

    producto = get_object_or_404(Producto, id=producto_id)

    precio = float(producto.precio)

    return render(request, 'catalogo/detalle_producto.html', {'producto': producto, 'precio': precio})






@staff_member_required
def crear_producto(request):

    if request.method == 'POST':

        form = ProductoForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            return redirect('catalogo:listar_productos')

    else:

        form = ProductoForm()

    return render(request, 'catalogo/crear_producto.html', {'form': form})


@staff_member_required
def agregar_producto(request):

    if request.method == 'POST':

        form = ProductoForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            messages.success(request, 'Producto agregado exitosamente.')

            return redirect('catalogo:listar_productos')

    else:

        form = ProductoForm()

    return render(request, 'catalogo/agregar_producto.html', {'form': form})


@method_decorator(staff_member_required, name='dispatch')
class ActualizarProductoView(UpdateView):

    model = Producto

    template_name = 'catalogo/actualizar_producto.html'

    fields = ['nombre', 'precio', 'descripcion']

    success_url = '/productos/'


def listar_productos(request):

    productos = Producto.objects.all().order_by('nombre')
    last_action = request.session.get('last_batch_action')
    return render(request, 'catalogo/productos.html', {'productos': productos, 'last_batch_action': last_action})   


@staff_member_required
def editar_producto(request, id):

    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':

        form = ProductoForm(request.POST, instance=producto)

        if form.is_valid():

            form.save()

            return redirect('catalogo:listar_productos')

    else:

        form = ProductoForm(instance=producto)

    return render(request, 'catalogo/editar_producto.html', {'form': form, 'producto': producto})


@staff_member_required
def actualizar_producto(request, pk):

    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':

        form = ProductoForm(request.POST, instance=producto)

        if form.is_valid():

            form.save()

            messages.success(request, f'Producto {producto.nombre} actualizado exitosamente.')

            return redirect('catalogo:listar_productos')

    else:

        form = ProductoForm(instance=producto)

    return render(request, 'catalogo/actualizar_producto.html', {'form': form})


@staff_member_required
def eliminar_productos(request):

    if request.method == 'POST':

        productos_ids = request.POST.getlist('productos')  

        if productos_ids:  

            Producto.objects.filter(id__in=productos_ids).delete()  

        return redirect('catalogo:listar_productos')  

    return redirect('catalogo:listar_productos')  


@staff_member_required
def marcar_productos(request):
    if request.method == 'POST':
        productos_ids = request.POST.getlist('productos')
        accion = request.POST.get('accion')
        if not productos_ids:
            messages.error(request, 'No seleccionaste productos.')
            return redirect('catalogo:listar_productos')

        qs = Producto.objects.filter(id__in=productos_ids)
        if accion == 'marcar_oferta':
            qs.update(oferta=True)
            messages.success(request, 'Productos marcados como oferta.')
        elif accion == 'quitar_oferta':
            qs.update(oferta=False)
            messages.success(request, 'Ofertas removidas de los productos.')
        elif accion == 'marcar_destacado':
            qs.update(destacado=True)
            messages.success(request, 'Productos marcados como destacados.')
        elif accion == 'quitar_destacado':
            qs.update(destacado=False)
            messages.success(request, 'Destacados removidos de los productos.')
        else:
            messages.error(request, 'Acción no reconocida.')

        # Log changes per producto
        try:
            from .models import ProductoCambio
            for p in qs:
                ProductoCambio.objects.create(producto=p, usuario=request.user if request.user.is_authenticated else None, accion=accion)
        except Exception:
            pass

        # Guardar acción en sesión para permitir deshacer
        request.session['last_batch_action'] = {'accion': accion, 'ids': productos_ids}
        request.session.modified = True

    return redirect('catalogo:listar_productos')


@staff_member_required
def deshacer_ultima_accion(request):
    last = request.session.get('last_batch_action')
    if not last:
        messages.error(request, 'No hay acción para deshacer.')
        return redirect('catalogo:listar_productos')

    accion = last.get('accion')
    ids = last.get('ids', [])
    qs = Producto.objects.filter(id__in=ids)
    reverse_map = {
        'marcar_oferta': ('oferta', False),
        'quitar_oferta': ('oferta', True),
        'marcar_destacado': ('destacado', False),
        'quitar_destacado': ('destacado', True),
    }
    if accion in reverse_map:
        field, value = reverse_map[accion]
        # Apply reverse
        update_kwargs = {field: value}
        qs.update(**update_kwargs)
        # Log undo
        try:
            from .models import ProductoCambio
            for p in qs:
                ProductoCambio.objects.create(producto=p, usuario=request.user if request.user.is_authenticated else None, accion='deshacer_'+accion)
        except Exception:
            pass
        # Clear session
        del request.session['last_batch_action']
        request.session.modified = True
        messages.success(request, 'La última acción fue deshecha.')
    else:
        messages.error(request, 'No se puede deshacer esta acción.')

    return redirect('catalogo:listar_productos')


@staff_member_required
def eliminar_producto(request, pk):

    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':

        producto.delete()

        return redirect('catalogo:listar_productos')  

    return render(request, 'catalogo/eliminar_producto.html', {'producto': producto})


@staff_member_required
def carga_masiva(request):

    if request.method == 'POST':

        csv_file = request.FILES.get('csv_file')

        if not csv_file or not csv_file.name.endswith('.csv'):

            messages.error(request, 'Por favor, sube un archivo CSV válido.')

            return redirect('catalogo:carga_masiva')


        try:

            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())

            for row in reader:

                if not all(field in row for field in ['nombre', 'descripcion', 'precio', 'stock']):

                    messages.error(request, 'El archivo CSV está incompleto.')

                    return redirect('catalogo:carga_masiva')


                try:

                    precio = float(row['precio'])

                    stock = int(row['stock'])

                except ValueError:

                    messages.error(request, 'El precio o el stock tienen un formato incorrecto.')

                    return redirect('catalogo:carga_masiva')


                Producto.objects.create(

                    nombre=row['nombre'],

                    descripcion=row['descripcion'],

                    precio=precio,

                    stock=stock

                )

            messages.success(request, 'Productos cargados correctamente.')

            return redirect('catalogo:listar_productos')

        except Exception as e:

            messages.error(request, f'Hubo un error al procesar el archivo: {e}')

            return redirect('catalogo:carga_masiva')

    return render(request, 'productos/carga_masiva.html')






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

    return redirect('catalogo:ver_carrito')


def agregar_al_carrito(request, producto_id):

    producto = get_object_or_404(Producto, id=producto_id)

    precio = float(producto.precio) if producto.precio else 0.0

    carrito = request.session.get('carrito', {})

    cantidad = request.POST.get('cantidad', 1)

    try:

        bytes_cantidad = max(1, int(cantidad))  

    except (ValueError, TypeError):

        bytes_cantidad = 1  


    producto_id_str = str(producto_id)  

    cantidad_disponible = producto.stock


    if producto_id_str in carrito:

        cantidad_total = carrito[producto_id_str].get('cantidad', 0) + bytes_cantidad

        if cantidad_total > cantidad_disponible:

            bytes_cantidad = cantidad_disponible - carrito[producto_id_str].get('cantidad', 0)

    else:

        if bytes_cantidad > cantidad_disponible:

            bytes_cantidad = cantidad_disponible  


    if bytes_cantidad > 0:

        if producto_id_str in carrito:

            carrito[producto_id_str]['cantidad'] += bytes_cantidad

        else:

            carrito[producto_id_str] = {

                'nombre': producto.nombre,

                'precio': float(precio),

                'cantidad': bytes_cantidad,

            }

        carrito[producto_id_str]['subtotal'] = float(carrito[producto_id_str]['precio']) * carrito[producto_id_str]['cantidad']  


    request.session['carrito'] = carrito

    request.session.modified = True  

    return redirect('catalogo:ver_carrito') 


def ver_carrito(request):

    carrito = request.session.get('carrito', {})
    items = []
    total = 0
    total_productos = 0
    mensajes_stock = []
    carrito_actualizado = {}

    for producto_id, datos in carrito.items():
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            continue

        if producto.stock == 0:
            continue

        cantidad = min(datos.get('cantidad', 0), producto.stock)
        if cantidad < datos.get('cantidad', 0):
            mensajes_stock.append(f"La cantidad de '{producto.nombre}' fue ajustada por stock.")

        precio_producto = float(producto.precio) if producto.precio else 0.0
        subtotal = cantidad * precio_producto

        items.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })

        total += subtotal
        total_productos += cantidad

        carrito_actualizado[producto_id] = {
            'nombre': producto.nombre,
            'precio': precio_producto,
            'cantidad': cantidad,
        }

    if carrito_actualizado != carrito:
        request.session['carrito'] = carrito_actualizado
        request.session.modified = True

    # Formulario de checkout integrado
    form = CheckoutForm()

    return render(request, 'catalogo/carrito_checkout.html', {
        'items': items,
        'total': total,
        'total_productos': total_productos,
        'mensaje_stock': "\n".join(mensajes_stock) if mensajes_stock else None,
        'form': form,
        'carrito': carrito,
    })


def actualizar_carrito(request, producto_id):

    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:

        cantidad = int(request.POST.get('cantidad', 1))

        if cantidad > 0:

            carrito[str(producto_id)]['cantidad'] = cantidad  

        else:

            del carrito[str(producto_id)]

    request.session['carrito'] = carrito

    request.session.modified = True  

    return redirect('catalogo:ver_carrito') 


def eliminar_del_carrito(request, producto_id, eliminar_todo=None):

    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:

        cantidad = carrito[str(producto_id)].get('cantidad', 0)

        if cantidad > 1 and not eliminar_todo:

            carrito[str(producto_id)]['cantidad'] -= 1

        else:

            del carrito[str(producto_id)]

        request.session['carrito'] = carrito

        request.session.modified = True

    return redirect('catalogo:ver_carrito')  


def some_view(request):

    return redirect(reverse('catalogo:ver_carrito'))


class CarritoView(View):

    def get(self, request):

        carrito = request.session.get('carrito', {})

        total = sum(float(item['precio']) * int(item['cantidad']) for item in carrito.values())

        return render(request, 'catalogo/carrito.html', {

            'carrito': carrito,

            'total': total

        })


def some_function():

    from .views import CarritoView  


def mostrar_carrito(request):

    carrito = request.session.get('carrito', {})

    total_general = sum(item.get('precio', 0) * item.get('cantidad', 0) for item in carrito.values())

    context = {

        'carrito': carrito,

        'total': total_general

    }

    return render(request, 'catalogo/checkout.html', context)






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


        mensaje = f"Nombre: {nombre}\nCorreo: {email}\nDirección: {direccion}\nMétodo: {metodo_pago}"

        send_mail('Nuevo contacto desde la tienda', mensaje, 'tienda@example.com', [email], fail_silently=False)

        return HttpResponse("Formulario procesado exitosamente.")

    return render(request, 'catalogo/contacto.html')


def procesar_envio(request):

    if request.method == 'POST':

        request.session['envio'] = request.POST['envio']

        return redirect('catalogo:procesar_pago')


def politicas_envio(request):

    if request.method == "POST":

        distancia = request.POST.get('distancia')

        if distancia:

            try:

                distancia = float(distancia)

            except ValueError:

                return HttpResponse("La distancia no es válida", status=400)

        else:

            return HttpResponse("La distancia no es válida", status=400)


        metodo_envio = request.POST.get('envio')

        costo_envio = calcular_costo_envio(metodo_envio, distancia)


        request.session['metodo_envio'] = metodo_envio

        request.session['distancia'] = distancia

        request.session['costo_envio'] = costo_envio

        return redirect('catalogo:confirmar_envio')


    return render(request, 'catalogo/politicas_envio.html')


def confirmar_envio(request):

    metodo_envio = request.session.get('metodo_envio')

    distancia = request.session.get('distancia')

    costo_envio = request.session.get('costo_envio')

    metodo_envio_display = get_metodo_envio_display(metodo_envio)

    return render(request, 'confirmar_envio.html', {

        'metodo_envio': metodo_envio_display,

        'distancia': distancia,

        'costo_envio': costo_envio,

    })






def finalizar_compra(request):


    carrito = Carrito.objects.filter(usuario=request.user).first() if request.user.is_authenticated else None

    if carrito and carrito.itemcarrito_set.exists():  

        return redirect('catalogo:checkout')  

    else:


        carrito_sesion = request.session.get('carrito', {})

        if carrito_sesion:

            return redirect('catalogo:checkout')

        messages.error(request, 'No hay productos en tu carrito.')  

        return redirect('catalogo:ver_carrito')  


def procesar_pago(request):

    if request.method == 'POST':

        request.session['carrito'] = {}

        messages.success(request, "Gracias por tu compra! Tu pedido ha sido procesado.")

        return redirect('catalogo:compra_exitosa', pedido_id=0)  

    return render(request, 'carrito/checkout.html')  


def checkout(request):

    carrito = request.session.get('carrito', {})

    productos = []

    totalCarrito = Decimal('0')


    for item in carrito.values():

        cantidad = int(item.get('cantidad', 0))

        precio = Decimal(str(item.get('precio', 0)))

        subtotal = precio * cantidad

        productos.append({

            'nombre': item.get('nombre'),

            'cantidad': cantidad,

            'precio': precio,

            'total': subtotal,

        })

        totalCarrito += subtotal


    if not productos:

        messages.warning(request, "Tu carrito está vacío. Agrega productos para continuar.")

        return redirect('catalogo:ver_carrito')

    form = CheckoutForm()

    return render(request, 'productos/checkout.html', {

        'totalCarrito': totalCarrito,

        'productos': productos,

        'carrito': carrito,

        'form': form,

    })


def procesar_compra(request):

    if request.method == 'POST':

        nombre = request.POST.get('nombre')

        direccion = request.POST.get('direccion')

        telefono = request.POST.get('telefono')

        metodo_pago = request.POST.get('metodo_pago')

        metodo_envio = request.POST.get('metodo_envio')

        return redirect('catalogo:checkout')

    return redirect('catalogo:ver_carrito')


def confirmar_compra(request):

    if request.method == "POST":

        nombre = request.POST.get("nombre")

        direccion = request.POST.get("direccion")

        telefono = request.POST.get("telefono")

        metodo_pago = request.POST.get("metodo_pago")

        metodo_envio = request.POST.get("metodo_envio")


        carrito = request.session.get("carrito", {})

        if not carrito:

            messages.error(request, "No hay productos para procesar la compra.")

            return redirect('catalogo:ver_carrito')


        nuevo_pedido = Pedido.objects.create(

            usuario=request.user if request.user.is_authenticated else None,

            total=Decimal('0'),

            metodo_pago=metodo_pago,

            nombre_contacto=nombre,

            telefono=telefono,

            direccion=direccion,

            metodo_envio=metodo_envio

        )


        total_pedido = Decimal('0')

        lineas_creadas = 0


        for prod_id, item in carrito.items():

            try:

                producto = Producto.objects.get(id=prod_id)

            except Producto.DoesNotExist:

                continue


            cantidad_solicitada = int(item.get('cantidad', 0))

            if cantidad_solicitada <= 0:

                continue


            cantidad_a_vender = min(cantidad_solicitada, producto.stock)

            if cantidad_a_vender == 0:

                messages.warning(request, f"El producto '{producto.nombre}' está agotado y no se incluyó en la compra.")

                continue


            if cantidad_a_vender < cantidad_solicitada:

                messages.warning(request, f"La cantidad de '{producto.nombre}' se ajustó a {cantidad_a_vender} por stock disponible.")


            LineaPedido.objects.create(

                pedido=nuevo_pedido,

                producto_nombre=producto.nombre,

                cantidad=cantidad_a_vender,

                precio_unitario=Decimal(str(item.get('precio', 0)))

            )


            producto.stock = max(producto.stock - cantidad_a_vender, 0)

            producto.save()


            total_pedido += Decimal(str(item.get('precio', 0))) * cantidad_a_vender

            lineas_creadas += 1


        if lineas_creadas == 0:

            messages.error(request, "No hay productos disponibles para completar la compra.")

            return redirect('catalogo:ver_carrito')


        nuevo_pedido.total = total_pedido

        nuevo_pedido.save()


        request.session["carrito"] = {}
        request.session.modified = True

        # Preparar datos para la boleta
        productos_boleta = []
        for prod_id, item in carrito.items():
            try:
                cantidad = int(item.get('cantidad', 0))
            except Exception:
                cantidad = 0
            precio = Decimal(str(item.get('precio', 0)))
            productos_boleta.append({
                'nombre': item.get('nombre'),
                'cantidad': cantidad,
                'total': float(precio * cantidad)
            })

        alias = request.POST.get('alias_mercado') or request.POST.get('alias_dni') or request.POST.get('alias_transferencia') or ''

        # Devolver boleta PDF directamente
        return generar_boleta(request, nombre, str(total_pedido), productos_boleta, metodo_pago, alias)

    return redirect('catalogo:ver_carrito')


def vista_orden(request):

    carrito_id = request.session.get('carrito_id')

    carrito = Carrito.objects.get(id=carrito_id) if carrito_id else None

    if request.method == 'POST':

        nombre_cliente = request.POST['nombre']

        direccion_cliente = request.POST['direccion']


        pedido = Pedido.objects.create(

            usuario=request.user if request.user.is_authenticated else None,

            nombre_contacto=nombre_cliente,

            direccion=direccion_cliente,

            total=0

        )

        return redirect('catalogo:confirmacion_orden', orden_id=pedido.id)

    return render(request, 'vista_orden.html', {'carrito': carrito})


def crear_orden(request):

    return redirect('catalogo:ver_carrito')


def confirmacion_orden(request, orden_id):

    return render(request, 'confirmacion_orden.html', {'orden_id': orden_id})


def orden_exitosa(request):

    return render(request, 'orden_exitosa.html')


def compra_exitosa(request, pedido_id=0):

    return render(request, 'compra_exitosa.html', {'pedido_id': pedido_id})
