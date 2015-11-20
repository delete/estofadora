# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='read',
            field=models.BooleanField(default=False, verbose_name='Lido'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='description',
            field=models.TextField(verbose_name='Mensagem'),
        ),
    ]
