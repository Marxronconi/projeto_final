# Generated by Django 4.2.21 on 2025-05-10 16:28

import core.models
from django.db import migrations, models
import django.db.models.deletion
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_divulgações'),
    ]

    operations = [
        migrations.CreateModel(
            name='Divulgacoes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('imagem', stdimage.models.StdImageField(blank=True, force_min_size=False, null=True, upload_to=core.models.get_file_path, variations={'thumb': {'crop': True, 'height': 720, 'width': 1280}}, verbose_name='Imagem')),
            ],
            options={
                'verbose_name': 'Divulgação',
                'verbose_name_plural': 'Divulgações',
            },
        ),
        migrations.AlterField(
            model_name='categoria',
            name='criado',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criação'),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='modificado',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualização'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='criado',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criação'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='modificado',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualização'),
        ),
        migrations.DeleteModel(
            name='Divulgações',
        ),
        migrations.AddField(
            model_name='divulgacoes',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.produto', verbose_name='Produto'),
        ),
    ]
