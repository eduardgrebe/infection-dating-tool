# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0015_diagnostictesthistoryrow_test_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='testpropertyestimate',
            name='diagnostic_delay_median',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='testpropertyestimate',
            name='time0_ref',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
