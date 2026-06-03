


from django.conf import settings

from django.db import migrations, models

import django.db.models.deletion



class Migration(migrations.Migration):


    dependencies = [

        migrations.swappable_dependency(settings.AUTH_USER_MODEL),

        ('catalogo', '0008_add_catalog_products'),

    ]


    operations = [

        migrations.AlterField(

            model_name='pedido',

            name='usuario',

            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),

        ),

    ]

