# Generated by Django 2.1.1 on 2019-11-14 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('distribucion', '0003_control_agregar_inventario_control_venta_distribucion_venta_distribucion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='control_agregar_inventario',
            name='distribuidor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Store.empleado'),
        ),
    ]
