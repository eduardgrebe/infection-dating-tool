# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-28 10:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0044_auto_20160628_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitdetail',
            name='earliest_visit_date',
            field=models.DateField(null=True),
        ),
    ]