# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0021_auto_20160429_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='architectavidityresult',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='architectavidityresultrow',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='architectavidityresultrow',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='architectunmodifiedresult',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='architectunmodifiedresultrow',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='architectunmodifiedresultrow',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bedresult',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bedresultrow',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bedresultrow',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bioradaviditycdcresult',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bioradaviditycdcresultrow',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bioradaviditycdcresultrow',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresultrow',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityjhuresult',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityjhuresultrow',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityjhuresultrow',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='geeniusresult',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='geeniusresultrow',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='geeniusresultrow',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='idev3result',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='idev3resultrow',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='idev3resultrow',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lagmaximresult',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lagmaximresultrow',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lagmaximresultrow',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lagsediaresult',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lagsediaresultrow',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lagsediaresultrow',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosdiluentresult',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosdiluentresultrow',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosdiluentresultrow',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosplasmaresult',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosplasmaresultrow',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosplasmaresultrow',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='luminexcdcresult',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='luminexcdcresultrow',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='luminexcdcresultrow',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresult',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresultrow',
            name='exclusion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresultrow',
            name='interpretation',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
