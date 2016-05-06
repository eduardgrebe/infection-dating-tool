# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0027_auto_20160505_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='architectavidityresult',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='architectunmodifiedresult',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bedresult',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bioradaviditycdcresult',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresult',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bioradavidityjhuresult',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='geeniusresult',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='idev3result',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='lagmaximresult',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='lagsediaresult',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='lsvitrosdiluentresult',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='lsvitrosplasmaresult',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='luminexcdcresult',
            name='recent_curtis_2013_alg35',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='luminexcdcresult',
            name='recent_curtis_2016_alg',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='luminexcdcresult',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='luminexcdcresultrow',
            name='luminex_result',
            field=models.ForeignKey(to='assay.LuminexCDCResult', null=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresult',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
