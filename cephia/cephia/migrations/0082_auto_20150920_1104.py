# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0081_auto_20150919_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsubject',
            name='cohort_entry_date',
            field=models.DateField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalsubject',
            name='subject_label',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='cohort_entry_date',
            field=models.DateField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='subject_label',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
    ]
