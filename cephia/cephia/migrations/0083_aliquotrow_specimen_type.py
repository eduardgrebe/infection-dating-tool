# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0082_auto_20150920_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='aliquotrow',
            name='specimen_type',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
