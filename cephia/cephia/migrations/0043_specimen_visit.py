# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0042_missingtransferoutrow'),
    ]

    operations = [
        migrations.AddField(
            model_name='specimen',
            name='visit',
            field=models.ForeignKey(blank=True, to='cephia.Visit', null=True),
        ),
    ]
