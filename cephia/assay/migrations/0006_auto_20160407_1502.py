# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0005_auto_20160407_1456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bioradaviditycdcresult',
            name='AI_recalc',
        ),
        migrations.RemoveField(
            model_name='bioradaviditycdcresultrow',
            name='AI_recalc',
        ),
        migrations.AddField(
            model_name='bioradaviditycdcresult',
            name='AI_reported',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='bioradaviditycdcresultrow',
            name='AI_reported',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
