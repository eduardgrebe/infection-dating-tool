# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0074_auto_20150907_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsubject',
            name='artificial',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subject',
            name='artificial',
            field=models.BooleanField(default=False),
        ),
    ]
