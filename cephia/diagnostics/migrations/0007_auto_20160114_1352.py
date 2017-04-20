# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0006_testpropertyestimate_foursigma_diagnostic_delay_days'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diagnostictesthistoryrow',
            old_name='test_name',
            new_name='test_code',
        ),
        migrations.AlterField(
            model_name='diagnostictesthistory',
            name='test_result',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
