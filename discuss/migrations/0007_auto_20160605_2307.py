# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-05 15:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discuss', '0006_discuss_reply_to'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discuss',
            options={'ordering': ('-create_at',)},
        ),
    ]
