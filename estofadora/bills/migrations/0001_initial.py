# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('date_to_pay', models.DateField(verbose_name='Dia')),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
                ('value', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Valor', default=0.0)),
                ('is_paid', models.BooleanField(verbose_name='Está paga?', default=False)),
            ],
            options={
                'verbose_name_plural': 'Contas',
                'ordering': ['date_to_pay'],
                'verbose_name': 'Conta',
            },
        ),
    ]
