# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0009_auto_20160114_1615'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='diagnostictest',
            table='cephia_diagnostic_tests',
        ),
        migrations.AlterModelTable(
            name='diagnostictesthistory',
            table='cephia_diagnostic_test_history',
        ),
        migrations.AlterModelTable(
            name='diagnostictesthistoryrow',
            table='cephia_diagnostic_test_history_row',
        ),
        migrations.AlterModelTable(
            name='protocollookup',
            table='cephia_protocol_lookup',
        ),
        migrations.AlterModelTable(
            name='testpropertyestimate',
            table='cephia_test_property_estimates',
        ),
    ]
