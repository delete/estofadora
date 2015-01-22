# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'cliente', 'ordering': ['date_join'], 'verbose_name_plural': 'clientes'},
        ),
    ]
