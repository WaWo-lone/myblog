# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-04-19 08:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20200419_1641'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlecolumn',
            options={'verbose_name_plural': '文章栏目'},
        ),
        migrations.AlterModelTable(
            name='articlecolumn',
            table='articlecolumn',
        ),
    ]
