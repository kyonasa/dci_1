# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 10:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('switch', '0011_l2ethservice'),
    ]

    operations = [
        migrations.AddField(
            model_name='l2ethservice',
            name='vxlanid',
            field=models.CharField(default=10010, max_length=30),
            preserve_default=False,
        ),
    ]
