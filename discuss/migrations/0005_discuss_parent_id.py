# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 08:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discuss', '0004_auto_20160530_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='discuss',
            name='parent_id',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='父评论id值'),
        ),
    ]
