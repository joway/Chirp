# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 03:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20160531_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(0, '管理员'), (1, '普通用户'), (2, '访客')], default=2, verbose_name='角色'),
        ),
    ]