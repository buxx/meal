# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-16 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(error_messages={'unique': 'Ce jour existe déjà'}, unique=True, verbose_name='Jour réservable')),
                ('cancelled', models.BooleanField(default=False)),
                ('price', models.CharField(max_length=255)),
            ],
        ),
    ]