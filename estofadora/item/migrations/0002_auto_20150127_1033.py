# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name_plural': 'Itens', 'verbose_name': 'Item'},
        ),
    ]
