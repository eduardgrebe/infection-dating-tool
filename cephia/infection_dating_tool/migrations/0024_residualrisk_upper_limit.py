# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-09-12 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infection_dating_tool', '0023_residualrisk_residual_risk_input'),
    ]

    operations = [
        migrations.AddField(
            model_name='residualrisk',
            name='upper_limit',
            field=models.FloatField(null=True),
        ),
    ]
