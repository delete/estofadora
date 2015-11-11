# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='public',
            field=models.BooleanField(default=False, verbose_name='Publico'),
        ),
        migrations.AddField(
            model_name='picture',
            name='state',
            field=models.CharField(default='before', choices=[('after', 'Depois'), ('before', 'Antes')], max_length=6, verbose_name='Estado'),
        ),
    ]
