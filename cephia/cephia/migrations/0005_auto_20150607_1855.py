# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0004_auto_20150605_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ethnicity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'cephia_ethnicity',
            },
        ),
        migrations.CreateModel(
            name='FileInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_file', models.FileField(upload_to=b'/home/jarryd/id/cephia/cephia/cephia/../../media')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(default=b'pending', max_length=8, choices=[(b'pending', b'Pending'), (b'imported', b'Imported'), (b'error', b'Error')])),
                ('message', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'cephia_fileinfo',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_label', models.CharField(max_length=255)),
                ('entry_date', models.DateField(null=True, blank=True)),
                ('entry_status', models.CharField(max_length=8, choices=[(b'negative', b'Negative'), (b'positive', b'Positive')])),
                ('last_negative_date', models.DateField(null=True, blank=True)),
                ('last_positive_date', models.DateField(null=True, blank=True)),
                ('ars_onset', models.DateField(null=True, blank=True)),
                ('fiebig', models.CharField(max_length=10)),
                ('dob', models.DateField(null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=6, choices=[(b'male', b'Male'), (b'female', b'Female'), (b'unkown', b'Unkown')])),
                ('sex_with_men', models.NullBooleanField()),
                ('sex_with_women', models.NullBooleanField()),
                ('iv_drug_user', models.NullBooleanField()),
                ('subtype_confirmed', models.NullBooleanField()),
                ('anti_retroviral_initiation_date', models.DateField(null=True, blank=True)),
                ('aids_diagnosis_date', models.DateField(null=True, blank=True)),
                ('treatment_interruption_date', models.DateField(null=True, blank=True)),
                ('treatment_resumption_date', models.DateField(null=True, blank=True)),
                ('country', models.ForeignKey(to='cephia.Country')),
                ('ethnicity', models.ForeignKey(to='cephia.Ethnicity')),
            ],
            options={
                'db_table': 'cephia_subject',
            },
        ),
        migrations.CreateModel(
            name='SubjectRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=9, choices=[(b'pending', b'Pending'), (b'processed', b'Processed'), (b'error', b'Error')])),
                ('error_message', models.TextField(blank=True)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('patient_label', models.CharField(max_length=255, blank=True)),
                ('entry_date', models.CharField(max_length=255, blank=True)),
                ('entry_status', models.CharField(max_length=255, blank=True)),
                ('country', models.CharField(max_length=255, blank=True)),
                ('last_negative_date', models.CharField(max_length=255, blank=True)),
                ('last_positive_date', models.CharField(max_length=255, blank=True)),
                ('ars_onset', models.CharField(max_length=255, blank=True)),
                ('fiebig', models.CharField(max_length=255, blank=True)),
                ('dob', models.CharField(max_length=255, blank=True)),
                ('gender', models.CharField(max_length=255, blank=True)),
                ('ethnicity', models.CharField(max_length=255, blank=True)),
                ('sex_with_men', models.CharField(max_length=255, blank=True)),
                ('sex_with_women', models.CharField(max_length=255, blank=True)),
                ('iv_drug_user', models.CharField(max_length=255, blank=True)),
                ('subtype_confirmed', models.CharField(max_length=255, blank=True)),
                ('subtype', models.CharField(max_length=255, blank=True)),
                ('anti_retroviral_initiation_date', models.CharField(max_length=255, blank=True)),
                ('aids_diagnosis_date', models.CharField(max_length=255, blank=True)),
                ('treatment_interruption_date', models.CharField(max_length=255, blank=True)),
                ('treatment_resumption_date', models.CharField(max_length=255, blank=True)),
                ('fileinfo', models.ForeignKey(to='cephia.FileInfo')),
            ],
            options={
                'db_table': 'cephia_subjectrow',
            },
        ),
        migrations.CreateModel(
            name='Subtype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'cephia_subtype',
            },
        ),
        migrations.AddField(
            model_name='subject',
            name='subtype',
            field=models.ForeignKey(to='cephia.Subtype'),
        ),
    ]
