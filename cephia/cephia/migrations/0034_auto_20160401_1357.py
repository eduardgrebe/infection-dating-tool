# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0033_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsubject',
            name='edsc_adjusted',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='edsc_adjusted',
            field=models.DateField(null=True, blank=True),
        ),
    ]
