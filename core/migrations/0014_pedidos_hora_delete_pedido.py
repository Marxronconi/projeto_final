# Generated by Django 4.2.21 on 2025-06-11 14:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_pedidos_options_pedidos_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='hora',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.DeleteModel(
            name='Pedido',
        ),
    ]
