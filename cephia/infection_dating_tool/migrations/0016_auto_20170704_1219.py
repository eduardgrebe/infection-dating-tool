# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-07-04 10:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('infection_dating_tool', '0015_auto_20170703_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selectedcategory',
            name='test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='infection_dating_tool.IDTDiagnosticTest'),
        ),
    ]
