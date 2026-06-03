from django import template

from django.templatetags.static import static


register = template.Library()


IMAGE_MAP = [

    ('hilo blanco', 'images/hilo_blanco.jpg'),

    ('hilo negro', 'images/hilo_negro.jpg'),

    ('hilo azul', 'images/hilo_azul.jpg'),

    ('hilo verde', 'images/hilo_verde.jpg'),

    ('hilo rojo', 'images/hilo_rojo.jpg'),

    ('hilo elast', 'images/hilo_elastico.jpg'),

    ('hilo nylon', 'images/hilo_azul.jpg'),

    ('hilo texturizado', 'images/hilo_verde.jpg'),

    ('hilo moulin', 'images/hilo_amarillo.jpg'),

    ('hilo', 'images/carretel_hilo.jpg'),

    ('aguja', 'images/aguja_maquina.jpg'),

    ('overlock', 'images/correas de overlock.jpg'),

    ('jeans', 'images/aguja_jeans.jpg'),

    ('prensatelas', 'images/pie-prensa-telas.jpg'),

    ('tijera', 'images/Tijeras.jpg'),

    ('canillas', 'images/carretel_hilo.jpg'),

    ('dedal', 'images/hilo_amarillo.jpg'),

    ('regla', 'images/tela_algodon.jpg'),

    ('alfiler', 'images/hilo_amarillo.jpg'),

    ('maquina', 'images/aguja_maquina.jpg'),

]

DEFAULT_IMAGE = 'images/cat_suerte.jpg'

DEFAULT_MEDIA_NAMES = ['productos/imagen_predeterminada.jpg', '']


@register.filter

def product_image(producto):

    nombre_imagen = getattr(producto, 'imagen', None)

    nombre_archivo = getattr(nombre_imagen, 'name', None)

    if nombre_archivo and nombre_archivo not in DEFAULT_MEDIA_NAMES:

        if nombre_archivo.startswith('images/'):

            return static(nombre_archivo)

        try:

            return producto.imagen.url

        except Exception:

            pass


    nombre = getattr(producto, 'nombre', '') or ''

    key = nombre.lower()

    for term, path in IMAGE_MAP:

        if term in key:

            return static(path)

    return static(DEFAULT_IMAGE)

