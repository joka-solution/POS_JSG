# Generated by Django 2.1.1 on 2019-11-14 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distribucion', '0004_auto_20191114_0212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='control_agregar_inventario',
            name='nombre',
            field=models.CharField(max_length=99999999),
        ),
    ]