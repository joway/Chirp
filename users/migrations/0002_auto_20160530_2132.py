# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-30 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='昵称'),
        ),
    ]
