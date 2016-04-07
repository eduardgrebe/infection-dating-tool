# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0025_auto_20160212_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjecteddi',
            name='edsc_days_difference',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
