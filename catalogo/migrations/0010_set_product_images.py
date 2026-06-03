from django.db import migrations



def set_product_images(apps, schema_editor):

    Producto = apps.get_model('catalogo', 'Producto')

    image_map = {

        'hilo de algodón': 'images/hilo_blanco.jpg',

        'hilo de poliéster': 'images/hilo_negro.jpg',

        'hilo nylon': 'images/hilo_azul.jpg',

        'hilo para overlock': 'images/correas de overlock.jpg',

        'hilo metálico': 'images/hilo_amarillo.jpg',

        'hilo encerado': 'images/hilo_amarillo.jpg',

        'hilo para jeans': 'images/hilo_jeans.jpg',

        'hilo bordado mate': 'images/hilo_amarillo.jpg',

        'hilo bordado brillante': 'images/hilo_amarillo.jpg',

        'hilo elástico': 'images/hilo_elastico.jpg',

        'agujas universales': 'images/aguja_maquina.jpg',

        'agujas punta bola': 'images/aguja-botonera.jpg',

        'agujas para jeans': 'images/aguja_jeans.jpg',

        'agujas dobles': 'images/aguja_maquina.jpg',

        'agujas para cuero': 'images/aguja_maquina.jpg',

        'canillas metálicas': 'images/carretel_hilo.jpg',

        'canillas plásticas': 'images/carretel_hilo.jpg',

        'prensatelas universal': 'images/pie-prensa-telas.jpg',

        'prensatelas zigzag': 'images/pie-prensa-telas.jpg',

        'prensatelas cremalleras': 'images/pie-prensa-telas.jpg',

        'prensatelas dobladillo invisible': 'images/pie-prensa-telas.jpg',

        'tijera de costura': 'images/Tijeras.jpg',

        'descosedor profesional': 'images/hilo_amarillo.jpg',

        'alfileres de cabeza': 'images/hilo_amarillo.jpg',

        'dedal de silicona': 'images/hilo_amarillo.jpg',

        'regla de costura': 'images/tela_algodon.jpg',

        'kit costura básico': 'images/carretel_hilo.jpg',

        'máquina de coser doméstica': 'images/aguja_maquina.jpg',

        'máquina de coser industrial': 'images/aguja_maquina.jpg',

        'hilo texturizado': 'images/hilo_verde.jpg',

        'hilo mouliné': 'images/hilo_amarillo.jpg',

    }


    for producto in Producto.objects.all():

        nombre = producto.nombre.lower()

        for clave, imagen in image_map.items():

            if clave in nombre:

                producto.imagen = imagen

                producto.save(update_fields=['imagen'])

                break



class Migration(migrations.Migration):

    dependencies = [

        ('catalogo', '0009_alter_pedido_usuario'),

    ]


    operations = [

        migrations.RunPython(set_product_images),

    ]

