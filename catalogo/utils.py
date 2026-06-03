


from .models import Producto


ENVIOS = {
    'domicilio': 'Envío a domicilio',
    'recoger_tienda': 'Retirar en tienda',
    'didi_moto': 'Envío con moto (Didi)',
    'uber_moto': 'Envío con moto (Uber)',
    'didi_auto': 'Envío con auto (Didi)',
    'uber_auto': 'Envío con auto (Uber)',
    'agencia': 'Envío por Agencia'
}


def calcular_costo_envio(metodo_envio, distancia):
    if metodo_envio == 'recoger_tienda':
        return 0
    if metodo_envio in ['didi_moto', 'uber_moto', 'didi_auto', 'uber_auto', 'domicilio']:
        if distancia <= 20:
            return 0
        if distancia <= 50:
            return 50
        return 'A consultar según distancia'
    if metodo_envio == 'agencia':
        if distancia > 50:
            return 'A consultar según agencia'
        return 'No disponible para distancias menores a 50 km'
    return 'A consultar'


def get_metodo_envio_display(metodo_envio):
    return ENVIOS.get(metodo_envio, metodo_envio or 'No seleccionado')


def obtener_carrito(session):

    """
    Recupera los productos del carrito almacenado en la sesión.
    
    Args:
        session (dict): La sesión del usuario.

    Returns:
        list: Una lista de productos en el carrito con sus cantidades.
    """

    carrito = session.get('carrito', {})

    productos_carrito = []


    for producto_id, item in carrito.items():

        try:

            producto = Producto.objects.get(id=producto_id)

            productos_carrito.append({

                'producto': producto,

                'cantidad': int(item['cantidad']),

            })

        except Producto.DoesNotExist:


            continue


    return productos_carrito


from django.core.mail import send_mail


def enviar_confirmacion_compra(usuario, orden):

    asunto = "Confirmación de tu compra"

    mensaje = f"""
    Hola {usuario.username},

    Gracias por tu compra en La Casa de Hilos y Repuestos.
    Tu pedido ha sido registrado con éxito.

    Detalles de tu pedido:
    - Total: ${orden.total}
    - Método de pago: {orden.metodo_pago}
    - Método de envío: {orden.metodo_envio}

    Nos pondremos en contacto contigo para la entrega.

    ¡Gracias por confiar en nosotros!
    """

    send_mail(asunto, mensaje, "tucorreo@tudominio.com", [usuario.email])

