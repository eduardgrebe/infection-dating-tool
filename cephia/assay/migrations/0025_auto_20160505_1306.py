# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0024_auto_20160504_1317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='luminexcdcresult',
            name='assay',
        ),
        migrations.RemoveField(
            model_name='luminexcdcresult',
            name='assay_result',
        ),
        migrations.RemoveField(
            model_name='luminexcdcresult',
            name='assay_run',
        ),
        migrations.RemoveField(
            model_name='luminexcdcresult',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='luminexcdcresult',
            name='specimen',
        ),
        migrations.RemoveField(
            model_name='luminexcdcresultrow',
            name='fileinfo',
        ),
        migrations.DeleteModel(
            name='LuminexCDCResult',
        ),
        migrations.DeleteModel(
            name='LuminexCDCResultRow',
        ),
    ]
