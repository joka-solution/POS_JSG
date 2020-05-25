# Generated by Django 2.1.1 on 2019-11-14 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('distribucion', '0007_inventario_distribucion_monto'),
    ]

    operations = [
        migrations.AddField(
            model_name='control_venta_distribucion',
            name='clienteid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='control_venta_distribucion',
            name='status',
            field=models.CharField(choices=[('Abierta', 'Abierta'), ('Pendiente', 'Pendiente'), ('Apartado', 'Apartado'), ('Cancelada', 'Cancelada'), ('Cerrada', 'Cerrada'), ('Concesion', 'Concesion'), ('Liquidado', 'Liquidado')], max_length=99999999, null=True),
        ),
        migrations.AlterField(
            model_name='control_venta_distribucion',
            name='distribuidor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Store.empleado'),
        ),
    ]
