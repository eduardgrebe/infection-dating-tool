# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0016_auto_20160426_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='architectavidityresult',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='architectunmodifiedresult',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bedresult',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bioradaviditycdcresult',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresult',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityjhuresult',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='geeniusresult',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='idev3result',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lagmaximresult',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lagsediaresult',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosdiluentresult',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosplasmaresult',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='luminexcdcresult',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresult',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
