# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0080_auto_20150919_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliquotrow',
            name='aliquot_label',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='aliquotrow',
            name='parent_label',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
    ]
