# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statement', '0002_balance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='balance',
            options={'verbose_name': 'Balance', 'verbose_name_plural': 'Balance', 'ordering': ['date']},
        ),
    ]
