# Generated by Django 3.1.4 on 2025-05-01 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('preco', models.IntegerField()),
                ('descricao', models.TextField()),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.categoria')),
            ],
        ),
    ]
