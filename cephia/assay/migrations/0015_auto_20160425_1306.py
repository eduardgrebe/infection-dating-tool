# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0014_auto_20160422_1338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='architectavidityresult',
            name='status',
        ),
        migrations.RemoveField(
            model_name='architectunmodifiedresult',
            name='status',
        ),
        migrations.RemoveField(
            model_name='bedresult',
            name='status',
        ),
        migrations.RemoveField(
            model_name='bioradaviditycdcresult',
            name='status',
        ),
        migrations.RemoveField(
            model_name='bioradavidityglasgowresult',
            name='status',
        ),
        migrations.RemoveField(
            model_name='bioradavidityjhuresult',
            name='status',
        ),
        migrations.RemoveField(
            model_name='geeniusresult',
            name='status',
        ),
        migrations.RemoveField(
            model_name='idev3result',
            name='status',
        ),
        migrations.RemoveField(
            model_name='lagmaximresult',
            name='status',
        ),
        migrations.RemoveField(
            model_name='lagsediaresult',
            name='status',
        ),
        migrations.RemoveField(
            model_name='lsvitrosdiluentresult',
            name='status',
        ),
        migrations.RemoveField(
            model_name='lsvitrosplasmaresult',
            name='status',
        ),
        migrations.RemoveField(
            model_name='luminexcdcresult',
            name='status',
        ),
        migrations.RemoveField(
            model_name='vitrosavidityresult',
            name='status',
        ),
        migrations.AddField(
            model_name='assayresult',
            name='warning_msg',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
