# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0008_auto_20160408_1159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bioradavidityjhuresult',
            name='AI_recalc',
        ),
        migrations.RemoveField(
            model_name='bioradavidityjhuresultrow',
            name='AI_recalc',
        ),
        migrations.AddField(
            model_name='bioradavidityjhuresult',
            name='AI_reported',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityjhuresultrow',
            name='AI_reported',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
