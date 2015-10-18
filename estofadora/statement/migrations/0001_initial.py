# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('date', models.DateField(verbose_name='Dia')),
                ('history', models.CharField(verbose_name='Histórico', max_length=100)),
                ('income', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Entrada', default=0.0)),
                ('expenses', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Saida', default=0.0)),
            ],
            options={
                'ordering': ['date'],
                'verbose_name': 'Cash',
                'verbose_name_plural': 'Cash',
            },
        ),
    ]
