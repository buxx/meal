# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-02 19:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0014_auto_20161102_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_day', models.DateField()),
                ('message', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='contactmessage',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.utcnow),
        ),
    ]
