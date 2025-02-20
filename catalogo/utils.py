

from .models import Producto

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
            # Si algún producto no existe, lo ignoramos
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
