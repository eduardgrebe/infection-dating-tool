# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0028_auto_20160217_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalvisitrow',
            name='artificial',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='visitrow',
            name='artificial',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
