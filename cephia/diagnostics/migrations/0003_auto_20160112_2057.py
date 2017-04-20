# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0002_diagnostictesthistory_diagnostictesthistoryrow_protocollookup_testpropertyestimate'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DiagnosticTestHistoryRow',
        ),
        migrations.AddField(
            model_name='diagnostictesthistory',
            name='test',
            field=models.ForeignKey(to='diagnostics.DiagnosticTest', null=True),
        ),
        migrations.AlterField(
            model_name='diagnostictesthistory',
            name='subject',
            field=models.ForeignKey(to='cephia.Subject', null=True),
        ),
    ]
