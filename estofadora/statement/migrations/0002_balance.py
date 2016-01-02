# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('date', models.DateField(verbose_name='Dia', unique=True)),
                ('value', models.DecimalField(default=0.0, decimal_places=2, verbose_name='Valor', max_digits=20)),
            ],
        ),
    ]
