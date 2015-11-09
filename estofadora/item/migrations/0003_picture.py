# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import estofadora.item.models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_auto_20150127_1033'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created_at', models.DateField(verbose_name='Criado em', auto_now_add=True)),
                ('image', models.ImageField(verbose_name='Imagem', upload_to=estofadora.item.models.image_path)),
                ('item', models.ForeignKey(to='item.Item', related_name='pictures')),
            ],
            options={
                'verbose_name': 'Imagem',
                'verbose_name_plural': 'Imagens',
            },
        ),
    ]
