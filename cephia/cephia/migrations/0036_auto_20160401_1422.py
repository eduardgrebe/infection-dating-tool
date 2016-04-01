# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0035_auto_20160401_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalsubject',
            name='edsc_adjusted',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='edsc_adjusted',
        ),
        migrations.AddField(
            model_name='subjecteddi',
            name='eddi_type',
            field=models.CharField(default='diagnostic_history', max_length=100),
            preserve_default=False,
        ),
    ]
