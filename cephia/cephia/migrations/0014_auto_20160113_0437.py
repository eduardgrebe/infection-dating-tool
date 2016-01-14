# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0013_auto_20151204_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsubject',
            name='eddi_max',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalsubject',
            name='eddi_mid_point_estimate',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalsubject',
            name='eddi_min',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='eddi_max',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='eddi_mid_point_estimate',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='eddi_min',
            field=models.DateField(null=True, blank=True),
        ),
    ]
