# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0014_auto_20150825_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specimen',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='transfer_reason',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='volume_units',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
