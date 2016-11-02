# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-17 16:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0004_auto_20161017_1629'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reservation',
            options={'ordering': ('day__date',)},
        ),
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together=set([('user', 'day')]),
        ),
    ]