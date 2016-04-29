# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0018_auto_20160428_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='architectavidityresult',
            name='warning_msg',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='architectunmodifiedresult',
            name='warning_msg',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bedresult',
            name='warning_msg',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bioradaviditycdcresult',
            name='warning_msg',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresult',
            name='warning_msg',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityjhuresult',
            name='warning_msg',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='geeniusresult',
            name='warning_msg',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='idev3result',
            name='warning_msg',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lagmaximresult',
            name='warning_msg',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lagsediaresult',
            name='warning_msg',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosdiluentresult',
            name='warning_msg',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosplasmaresult',
            name='warning_msg',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='luminexcdcresult',
            name='warning_msg',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresult',
            name='warning_msg',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
