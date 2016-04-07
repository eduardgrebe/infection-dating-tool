# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0014_diagnostictesthistory_ignore'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnostictesthistoryrow',
            name='test_history',
            field=models.ForeignKey(to='diagnostics.DiagnosticTestHistory', null=True),
        ),
    ]
