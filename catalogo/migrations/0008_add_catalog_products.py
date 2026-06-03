from django.db import migrations, models



def create_catalog_products(apps, schema_editor):

    Producto = apps.get_model('catalogo', 'Producto')

    products = [

        {

            'nombre': 'Hilo de algodón 100m blanco',

            'descripcion': 'Hilo de algodón suave para costura general y patchwork.',

            'precio': '120.00',

            'stock': 50,

        },

        {

            'nombre': 'Hilo de poliéster 100m negro',

            'descripcion': 'Hilo resistente de poliéster para costura diaria y reposición.',

            'precio': '130.00',

            'stock': 45,

        },

        {

            'nombre': 'Hilo nylon invisible 50m',

            'descripcion': 'Hilo transparente ideal para costura en telas delicadas y dobladillos invisibles.',

            'precio': '180.00',

            'stock': 40,

        },

        {

            'nombre': 'Hilo para overlock 200m gris',

            'descripcion': 'Hilo suave y flexible para remalladoras y costura en bordes.',

            'precio': '210.00',

            'stock': 35,

        },

        {

            'nombre': 'Hilo metálico dorado 100m',

            'descripcion': 'Hilo decorativo metálico para bordados y aplicaciones brillantes.',

            'precio': '280.00',

            'stock': 25,

        },

        {

            'nombre': 'Hilo encerado 100m',

            'descripcion': 'Hilo encerado para manualidades, tapicería ligera y costura resistente.',

            'precio': '190.00',

            'stock': 30,

        },

        {

            'nombre': 'Hilo para jeans 100m azul',

            'descripcion': 'Hilo fuerte para tejidos pesados como jeans y mezclilla.',

            'precio': '150.00',

            'stock': 40,

        },

        {

            'nombre': 'Hilo bordado mate 100m',

            'descripcion': 'Hilo para bordado de acabado mate y colores intensos.',

            'precio': '170.00',

            'stock': 32,

        },

        {

            'nombre': 'Hilo bordado brillante 100m',

            'descripcion': 'Hilo para bordado con brillo suave y alta cobertura.',

            'precio': '190.00',

            'stock': 28,

        },

        {

            'nombre': 'Hilo elástico 50m',

            'descripcion': 'Hilo elástico para costura de ropa deportiva y prendas ajustadas.',

            'precio': '160.00',

            'stock': 36,

        },

        {

            'nombre': 'Agujas universales 90/14 x10',

            'descripcion': 'Pack de agujas universales para máquina de coser doméstica.',

            'precio': '220.00',

            'stock': 50,

        },

        {

            'nombre': 'Agujas punta bola 75/11 x10',

            'descripcion': 'Pack de agujas para telas delicadas como seda y jerseys.',

            'precio': '240.00',

            'stock': 38,

        },

        {

            'nombre': 'Agujas para jeans 100/16 x10',

            'descripcion': 'Agujas especiales para tejidos pesados como denim y lona.',

            'precio': '260.00',

            'stock': 30,

        },

        {

            'nombre': 'Agujas dobles 4.0mm x2',

            'descripcion': 'Agujas dobles para costura decorativa y dobladillos elásticos.',

            'precio': '290.00',

            'stock': 20,

        },

        {

            'nombre': 'Agujas para cuero 110/18 x10',

            'descripcion': 'Agujas reforzadas para coser cuero, ecocuero y materiales gruesos.',

            'precio': '320.00',

            'stock': 26,

        },

        {

            'nombre': 'Canillas metálicas x10',

            'descripcion': 'Pack de canillas metálicas para máquinas de coser domésticas.',

            'precio': '120.00',

            'stock': 60,

        },

        {

            'nombre': 'Canillas plásticas x10',

            'descripcion': 'Canillas plásticas compatibles con la mayoría de máquinas de coser.',

            'precio': '100.00',

            'stock': 55,

        },

        {

            'nombre': 'Prensatelas universal',

            'descripcion': 'Prensatelas estándar para costura cotidiana en máquina doméstica.',

            'precio': '470.00',

            'stock': 22,

        },

        {

            'nombre': 'Prensatelas zigzag',

            'descripcion': 'Prensatelas para puntadas zigzag y decorativas.',

            'precio': '470.00',

            'stock': 18,

        },

        {

            'nombre': 'Prensatelas cremalleras',

            'descripcion': 'Prensatelas especial para coser cremalleras con facilidad.',

            'precio': '520.00',

            'stock': 16,

        },

        {

            'nombre': 'Prensatelas dobladillo invisible',

            'descripcion': 'Prensatelas para dobladillos invisibles en telas finas y mantas.',

            'precio': '520.00',

            'stock': 18,

        },

        {

            'nombre': 'Tijera de costura 8 pulgadas',

            'descripcion': 'Tijera de alta precisión para cortar telas y patrones.',

            'precio': '850.00',

            'stock': 40,

        },

        {

            'nombre': 'Descosedor profesional',

            'descripcion': 'Descosedor para retirar costuras con seguridad y precisión.',

            'precio': '220.00',

            'stock': 45,

        },

        {

            'nombre': 'Alfileres de cabeza de vidrio x50',

            'descripcion': 'Alfileres resistentes con cabeza de vidrio para sujetar telas finas.',

            'precio': '130.00',

            'stock': 65,

        },

        {

            'nombre': 'Dedal de silicona',

            'descripcion': 'Dedal ergonómico para proteger el dedo al coser a mano.',

            'precio': '90.00',

            'stock': 70,

        },

        {

            'nombre': 'Regla de costura 50cm',

            'descripcion': 'Regla transparente para marcación y medición en costura.',

            'precio': '145.00',

            'stock': 48,

        },

        {

            'nombre': 'Kit costura básico',

            'descripcion': 'Kit con agujas, hilos, botones y accesorios para costura de emergencia.',

            'precio': '360.00',

            'stock': 38,

        },

        {

            'nombre': 'Máquina de coser doméstica mecánica',

            'descripcion': 'Máquina de coser para uso doméstico con puntadas básicas y medición de tela.',

            'precio': '28500.00',

            'stock': 12,

        },

        {

            'nombre': 'Máquina de coser industrial recta',

            'descripcion': 'Máquina industrial recta para costura pesada y producción de taller.',

            'precio': '62000.00',

            'stock': 5,

        },

        {

            'nombre': 'Hilo texturizado 100m verde',

            'descripcion': 'Hilo texturizado para costuras decorativas y bordado creativo.',

            'precio': '175.00',

            'stock': 30,

        },

        {

            'nombre': 'Hilo mouliné 25m multicolor',

            'descripcion': 'Hilo mouliné para bordado a mano con colores vibrantes.',

            'precio': '140.00',

            'stock': 34,

        }

    ]


    for producto in products:

        Producto.objects.get_or_create(

            nombre=producto['nombre'],

            defaults={

                'descripcion': producto['descripcion'],

                'precio': producto['precio'],

                'stock': producto['stock'],

            }

        )



def delete_catalog_products(apps, schema_editor):

    Producto = apps.get_model('catalogo', 'Producto')

    nombres = [

        'Hilo de algodón 100m blanco',

        'Hilo de poliéster 100m negro',

        'Hilo nylon invisible 50m',

        'Hilo para overlock 200m gris',

        'Hilo metálico dorado 100m',

        'Hilo encerado 100m',

        'Hilo para jeans 100m azul',

        'Hilo bordado mate 100m',

        'Hilo bordado brillante 100m',

        'Hilo elástico 50m',

        'Agujas universales 90/14 x10',

        'Agujas punta bola 75/11 x10',

        'Agujas para jeans 100/16 x10',

        'Agujas dobles 4.0mm x2',

        'Agujas para cuero 110/18 x10',

        'Canillas metálicas x10',

        'Canillas plásticas x10',

        'Prensatelas universal',

        'Prensatelas zigzag',

        'Prensatelas cremalleras',

        'Prensatelas dobladillo invisible',

        'Tijera de costura 8 pulgadas',

        'Descosedor profesional',

        'Alfileres de cabeza de vidrio x50',

        'Dedal de silicona',

        'Regla de costura 50cm',

        'Kit costura básico',

        'Máquina de coser doméstica mecánica',

        'Máquina de coser industrial recta',

        'Hilo texturizado 100m verde',

        'Hilo mouliné 25m multicolor'

    ]

    Producto.objects.filter(nombre__in=nombres).delete()



class Migration(migrations.Migration):


    dependencies = [

        ('catalogo', '0007_categoria_lineapedido_remove_ordenview_carrito_and_more'),

    ]


    operations = [

        migrations.RunPython(create_catalog_products, delete_catalog_products),

    ]

