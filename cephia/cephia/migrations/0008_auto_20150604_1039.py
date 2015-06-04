# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0007_auto_20150604_1032'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_label', models.CharField(max_length=255)),
                ('entry_date', models.CharField(max_length=255)),
                ('entry_status', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('last_negative_date', models.CharField(max_length=255)),
                ('last_positive_date', models.CharField(max_length=255)),
                ('ars_onset', models.CharField(max_length=255)),
                ('fiebig', models.CharField(max_length=255)),
                ('dob', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=255)),
                ('ethnicity', models.CharField(max_length=255)),
                ('sex_with_men', models.CharField(max_length=255)),
                ('sex_with_women', models.CharField(max_length=255)),
                ('iv_drug_user', models.CharField(max_length=255)),
                ('subtype_confirmed', models.CharField(max_length=255)),
                ('subtype', models.CharField(max_length=255)),
                ('anti_retroviral_initiation_date', models.CharField(max_length=255)),
                ('aids_diagnosis_date', models.CharField(max_length=255)),
                ('treatment_interruption_date', models.CharField(max_length=255)),
                ('treatment_resumption_date', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cephia_subject',
            },
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='state',
            field=models.CharField(default=b'pending', max_length=8, choices=[(b'pending', b'Pending'), (b'imported', b'Imported'), (b'error', b'Error')]),
        ),
        migrations.AlterModelTable(
            name='subjectrow',
            table='cephia_subjectrow',
        ),
    ]
