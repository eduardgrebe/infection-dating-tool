# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0062_auto_20150826_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalFileInfo',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('data_file', models.TextField(max_length=100)),
                ('file_type', models.CharField(max_length=20, choices=[(b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In'), (b'transfer_out', b'Transfer Out'), (b'missing_transfer_out', b'Missing Transfer Out'), (b'aliquot', b'Aliquot')])),
                ('created', models.DateTimeField(editable=False, blank=True)),
                ('state', models.CharField(default=b'pending', max_length=10, choices=[(b'pending', b'Pending'), (b'imported', b'Imported'), (b'validated', b'Validated'), (b'error', b'Error')])),
                ('priority', models.IntegerField(default=1)),
                ('message', models.TextField(blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical file info',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSpecimen',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('specimen_label', models.CharField(max_length=255, null=True, blank=True)),
                ('parent_label', models.CharField(max_length=255, null=True, blank=True)),
                ('number_of_containers', models.IntegerField(null=True, blank=True)),
                ('reported_draw_date', models.DateField(null=True, blank=True)),
                ('transfer_in_date', models.DateField(null=True, blank=True)),
                ('transfer_out_date', models.DateField(null=True, blank=True)),
                ('created_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified_date', models.DateField(null=True, blank=True)),
                ('transfer_reason', models.CharField(max_length=50, null=True, blank=True)),
                ('volume', models.FloatField(null=True, blank=True)),
                ('volume_units', models.CharField(max_length=20, null=True, blank=True)),
                ('initial_claimed_volume', models.FloatField(null=True, blank=True)),
                ('aliquoting_reason', models.CharField(max_length=20, null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('receiving_site', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.Site', null=True)),
                ('source_study', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.Study', null=True)),
                ('specimen_type', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.SpecimenType', null=True)),
                ('subject', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.Subject', null=True)),
                ('visit', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.Visit', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical specimen',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSubject',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('subject_label', models.CharField(max_length=255, null=True, blank=True)),
                ('cohort_entry_date', models.DateField(null=True, blank=True)),
                ('cohort_entry_hiv_status', models.CharField(max_length=8, choices=[(b'negative', b'Negative'), (b'positive', b'Positive')])),
                ('last_negative_date', models.DateField(null=True, blank=True)),
                ('first_positive_date', models.DateField(null=True, blank=True)),
                ('ars_onset_date', models.DateField(null=True, blank=True)),
                ('fiebig_stage_at_firstpos', models.CharField(max_length=10)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('date_of_death', models.DateField(null=True, blank=True)),
                ('sex', models.CharField(blank=True, max_length=6, choices=[(b'male', b'Male'), (b'female', b'Female'), (b'unkown', b'Unkown')])),
                ('transgender', models.NullBooleanField()),
                ('risk_sex_with_men', models.NullBooleanField()),
                ('risk_sex_with_women', models.NullBooleanField()),
                ('risk_idu', models.NullBooleanField()),
                ('subtype_confirmed', models.NullBooleanField()),
                ('art_initiation_date', models.DateField(null=True, blank=True)),
                ('aids_diagnosis_date', models.DateField(null=True, blank=True)),
                ('art_interruption_date', models.DateField(null=True, blank=True)),
                ('art_resumption_date', models.DateField(null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('country', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.Country', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('population_group', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.Ethnicity', null=True)),
                ('subtype', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.Subtype', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical subject',
            },
        ),
        migrations.CreateModel(
            name='HistoricalVisit',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('subject_label', models.CharField(max_length=255)),
                ('visit_date', models.DateField(null=True, blank=True)),
                ('visit_hivstatus', models.CharField(max_length=8, choices=[(b'negative', b'Negative'), (b'positive', b'Positive'), (b'unknown', b'Unkown')])),
                ('cd4_count', models.IntegerField(null=True)),
                ('vl', models.CharField(max_length=10, null=True)),
                ('scopevisit_ec', models.CharField(max_length=100, null=True)),
                ('pregnant', models.NullBooleanField()),
                ('hepatitis', models.NullBooleanField()),
                ('artificial', models.BooleanField(default=False)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('source_study', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.Study', null=True)),
                ('subject', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.Subject', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical visit',
            },
        ),
    ]
