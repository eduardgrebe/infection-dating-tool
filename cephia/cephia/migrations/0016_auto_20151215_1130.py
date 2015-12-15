# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0015_auto_20151211_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileinfo',
            name='panel_type',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='historicalfileinfo',
            name='panel_type',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]
