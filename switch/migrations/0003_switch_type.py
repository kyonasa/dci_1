# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 01:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('switch', '0002_tunnel'),
    ]

    operations = [
        migrations.AddField(
            model_name='switch',
            name='type',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]
