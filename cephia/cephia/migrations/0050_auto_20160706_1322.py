# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-06 11:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0049_auto_20160705_1226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalspecimen',
            old_name='is_artificicial',
            new_name='is_artificial',
        ),
        migrations.RenameField(
            model_name='specimen',
            old_name='is_artificicial',
            new_name='is_artificial',
        ),
    ]
