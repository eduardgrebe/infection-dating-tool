# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0005_auto_20151015_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalspecimen',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
