# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-29 09:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0059_auto_20160829_1146'),
    ]

    operations = [
        migrations.RenameField(
            model_name='viralloadrow',
            old_name='viral_load',
            new_name='value',
        ),
    ]