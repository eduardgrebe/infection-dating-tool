# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-30 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0073_auto_20161129_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='cephiauser',
            name='password_reset_token',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True),
        ),
    ]