# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0079_auto_20150918_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalspecimen',
            name='specimen_label',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalspecimen',
            name='subject_label',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='specimen_label',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='subject_label',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
    ]
