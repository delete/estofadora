# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20150122_1116'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='Nome', max_length=256)),
                ('description', models.TextField(verbose_name='')),
                ('concluded', models.BooleanField(verbose_name='Concluido', default=False)),
                ('arrived_date', models.DateTimeField(verbose_name='Chegou', auto_now_add=True)),
                ('delivery_date', models.DateTimeField(verbose_name='Entrega')),
                ('total_value', models.DecimalField(verbose_name='Valor total', max_digits=20, default=0.0, decimal_places=2)),
                ('total_paid', models.DecimalField(verbose_name='Valor pago', max_digits=20, default=0.0, decimal_places=2)),
                ('client', models.ForeignKey(to='client.Client', related_name='client')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
            bases=(models.Model,),
        ),
    ]
