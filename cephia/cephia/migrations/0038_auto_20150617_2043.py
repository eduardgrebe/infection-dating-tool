# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0037_auto_20150617_1904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specimen',
            name='label',
        ),
        migrations.AddField(
            model_name='specimen',
            name='aliquoting_reason',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='annihilation_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='child_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='created_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='modified_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='panel_inclusion_criteria',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='parent_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
