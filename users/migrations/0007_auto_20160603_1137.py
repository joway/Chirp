# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-03 03:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_index=True, default='', max_length=255, verbose_name='昵称'),
        ),
    ]
