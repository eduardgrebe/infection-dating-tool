# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0007_auto_20151022_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalspecimen',
            name='shipped_in_panel',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='shipped_in_panel',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
