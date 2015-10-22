# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0006_auto_20151022_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsubject',
            name='edsc_reported',
            field=models.DateField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='edsc_reported',
            field=models.DateField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subjectrow',
            name='edsc_reported_dd',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='subjectrow',
            name='edsc_reported_mm',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='subjectrow',
            name='edsc_reported_yyyy',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
