# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 04:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('switch', '0007_auto_20170227_0438'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='P',
            field=models.CharField(default=24, max_length=30),
            preserve_default=False,
        ),
    ]
