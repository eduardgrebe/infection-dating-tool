# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0008_auto_20150604_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjectrow',
            name='aids_diagnosis_date',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='anti_retroviral_initiation_date',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='ars_onset',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='country',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='dob',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='entry_date',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='entry_status',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='ethnicity',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='fiebig',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='gender',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='iv_drug_user',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='last_negative_date',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='last_positive_date',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='patient_label',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='sex_with_men',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='sex_with_women',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='subtype',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='subtype_confirmed',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='treatment_interruption_date',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='treatment_resumption_date',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
