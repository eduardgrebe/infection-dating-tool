# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0005_auto_20160114_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='testpropertyestimate',
            name='foursigma_diagnostic_delay_days',
            field=models.IntegerField(null=True),
        ),
    ]
