# Generated by Django 2.1.1 on 2019-11-14 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distribucion', '0006_auto_20191114_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventario_distribucion',
            name='monto',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
