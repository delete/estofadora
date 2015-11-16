# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Nome', max_length=200)),
                ('email', models.CharField(verbose_name='Email', blank=True, null=True, max_length=200)),
                ('telephone', models.CharField(verbose_name='Telefone', blank=True, null=True, max_length=15)),
                ('subject', models.CharField(verbose_name='Assunto', max_length=30)),
                ('description', models.TextField(verbose_name='')),
                ('created_at', models.DateTimeField(verbose_name='Criado em', auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
    ]
