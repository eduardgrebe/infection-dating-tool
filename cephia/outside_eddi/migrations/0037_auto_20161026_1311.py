# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-26 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outside_eddi', '0036_auto_20161026_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outsideeddifileinfo',
            name='data_file',
            field=models.FileField(upload_to='outside_eddi_uploads'),
        ),
    ]
