# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
                ('email', models.EmailField(max_length=75, blank=True, verbose_name='Email', unique=True)),
                ('adress', models.CharField(max_length=256, verbose_name='Endereço')),
                ('telephone1', models.CharField(max_length=15, verbose_name='Telefone 1')),
                ('telephone2', models.CharField(max_length=15, blank=True, verbose_name='Telefone 2')),
                ('is_active', models.BooleanField(default=True, verbose_name='Está ativo?')),
                ('date_join', models.DateTimeField(verbose_name='Data de cadastro', auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
