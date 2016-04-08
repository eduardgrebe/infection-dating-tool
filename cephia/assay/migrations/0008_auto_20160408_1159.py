# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0007_auto_20160408_1157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bioradavidityglasgowresult',
            name='AI_recalc',
        ),
        migrations.RemoveField(
            model_name='bioradavidityglasgowresultrow',
            name='AI_recalc',
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresult',
            name='AI_reported',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresultrow',
            name='AI_reported',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
