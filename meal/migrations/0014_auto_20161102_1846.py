# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-02 18:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0013_auto_20161102_1845'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactmessage',
            options={'ordering': ['-created']},
        ),
    ]
