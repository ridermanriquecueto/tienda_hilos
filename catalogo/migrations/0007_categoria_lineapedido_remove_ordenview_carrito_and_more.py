


from django.db import migrations, models

import django.db.models.deletion



class Migration(migrations.Migration):


    dependencies = [

        ('catalogo', '0006_remove_pedido_carrito_remove_pedido_estado_and_more'),

    ]


    operations = [

        migrations.CreateModel(

            name='Categoria',

            fields=[

                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),

                ('nombre', models.CharField(max_length=100, unique=True)),

                ('descripcion', models.TextField(blank=True, null=True)),

            ],

            options={

                'verbose_name': 'Categoría',

                'verbose_name_plural': 'Categorías',

            },

        ),

        migrations.CreateModel(

            name='LineaPedido',

            fields=[

                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),

                ('producto_nombre', models.CharField(max_length=255)),

                ('cantidad', models.PositiveIntegerField()),

                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),

            ],

        ),

        migrations.RemoveField(

            model_name='ordenview',

            name='carrito',

        ),

        migrations.AlterModelOptions(

            name='carrito',

            options={'verbose_name': 'Carrito', 'verbose_name_plural': 'Carritos'},

        ),

        migrations.AlterModelOptions(

            name='pedido',

            options={'verbose_name': 'Pedido', 'verbose_name_plural': 'Pedidos'},

        ),

        migrations.RenameField(

            model_name='pedido',

            old_name='nombre',

            new_name='nombre_contacto',

        ),

        migrations.RemoveField(

            model_name='carrito',

            name='total',

        ),

        migrations.RemoveField(

            model_name='pedido',

            name='comprobante_pago',

        ),

        migrations.RemoveField(

            model_name='pedido',

            name='estado_envio',

        ),

        migrations.RemoveField(

            model_name='pedido',

            name='estado_pago',

        ),

        migrations.AddField(

            model_name='pedido',

            name='estado',

            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('completada', 'Completada'), ('cancelada', 'Cancelada')], default='pendiente', max_length=20),

        ),

        migrations.AddField(

            model_name='pedido',

            name='tipo_venta',

            field=models.CharField(choices=[('minorista', 'Minorista'), ('mayorista', 'Mayorista')], default='minorista', max_length=50),

        ),

        migrations.AlterField(

            model_name='pedido',

            name='metodo_envio',

            field=models.CharField(choices=[('domicilio', 'Domicilio'), ('recoger', 'Recoger en tienda')], default='domicilio', max_length=50),

        ),

        migrations.AlterField(

            model_name='pedido',

            name='metodo_pago',

            field=models.CharField(choices=[('mercado_pago', 'Mercado Pago'), ('transferencia', 'Transferencia Bancaria'), ('tarjeta', 'Tarjeta de Crédito')], max_length=50),

        ),

        migrations.DeleteModel(

            name='Orden',

        ),

        migrations.DeleteModel(

            name='OrdenView',

        ),

        migrations.AddField(

            model_name='lineapedido',

            name='pedido',

            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineas', to='catalogo.pedido'),

        ),

        migrations.AddField(

            model_name='producto',

            name='categoria',

            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productos', to='catalogo.categoria'),

        ),

    ]

