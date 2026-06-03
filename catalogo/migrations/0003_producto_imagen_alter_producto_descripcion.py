


from django.db import migrations, models



class Migration(migrations.Migration):


    dependencies = [

        ('catalogo', '0002_alter_carrito_options_alter_producto_descripcion_and_more'),

    ]


    operations = [

        migrations.AddField(

            model_name='producto',

            name='imagen',

            field=models.ImageField(default='productos/imagen_predeterminada.jpg', upload_to='productos/'),

        ),

        migrations.AlterField(

            model_name='producto',

            name='descripcion',

            field=models.CharField(default='Descripción predeterminada', max_length=255),

        ),

    ]

