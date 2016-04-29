# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0017_auto_20160426_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='bedresult',
            name='well',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AddField(
            model_name='bedresultrow',
            name='well',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
