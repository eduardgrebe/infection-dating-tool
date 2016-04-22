# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0012_auto_20160422_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='lsvitrosdiluentresult',
            name='final_SCO',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosdiluentresult',
            name='well',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='lsvitrosdiluentresultrow',
            name='final_SCO',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='lsvitrosdiluentresultrow',
            name='well',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='lsvitrosplasmaresult',
            name='final_SCO',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosplasmaresult',
            name='well',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='lsvitrosplasmaresultrow',
            name='final_SCO',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='lsvitrosplasmaresultrow',
            name='well',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
