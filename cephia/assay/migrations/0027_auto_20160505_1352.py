# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0026_luminexcdcresult_luminexcdcresultrow'),
    ]

    operations = [
        migrations.AddField(
            model_name='luminexcdcresultrow',
            name='well_treated',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='luminexcdcresultrow',
            name='well_untreated',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
