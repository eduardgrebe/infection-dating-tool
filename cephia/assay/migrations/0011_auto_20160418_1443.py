# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0010_auto_20160408_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='architectavidityresult',
            name='status',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='architectunmodifiedresult',
            name='status',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='bedresult',
            name='status',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='bioradaviditycdcresult',
            name='status',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresult',
            name='status',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='bioradavidityjhuresult',
            name='status',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='geeniusresult',
            name='status',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='idev3result',
            name='status',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='lagmaximresult',
            name='status',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='lagsediaresult',
            name='status',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='lsvitrosdiluentresult',
            name='status',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='lsvitrosplasmaresult',
            name='status',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='luminexcdcresult',
            name='status',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresult',
            name='status',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
