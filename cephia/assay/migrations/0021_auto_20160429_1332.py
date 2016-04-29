# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0020_auto_20160429_1140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bioradavidityglasgowresult',
            name='classification',
        ),
        migrations.RemoveField(
            model_name='bioradavidityglasgowresult',
            name='untreated_dilwashsoln_OD',
        ),
        migrations.RemoveField(
            model_name='bioradavidityglasgowresult',
            name='well_untreated_dilwashsoln',
        ),
        migrations.RemoveField(
            model_name='bioradavidityglasgowresultrow',
            name='classification',
        ),
        migrations.RemoveField(
            model_name='bioradavidityglasgowresultrow',
            name='untreated_dilwashsoln_OD',
        ),
        migrations.RemoveField(
            model_name='bioradavidityglasgowresultrow',
            name='well_untreated_dilwashsoln',
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresult',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresult',
            name='untreated_buffer_OD',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresult',
            name='well_untreated_buffer',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresultrow',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresultrow',
            name='untreated_buffer_OD',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresultrow',
            name='well_untreated_buffer',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresult',
            name='dilution',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresult',
            name='well_treated_urea',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresultrow',
            name='dilution',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresultrow',
            name='well_treated_urea',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
