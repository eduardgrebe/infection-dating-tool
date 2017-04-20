# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0030_auto_20160405_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsubject',
            name='fiebig_stage_at_firstpos',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='fiebig_stage_at_firstpos',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
