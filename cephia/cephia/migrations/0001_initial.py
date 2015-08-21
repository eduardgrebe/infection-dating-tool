# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.contrib.auth.models
import django.utils.timezone
import django.core.validators
import lib.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='CephiaUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'cephia_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AliquotingReason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cephia_aliquoting_reason',
            },
        ),
        migrations.CreateModel(
            name='AnnihilationRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'processed', b'Processed'), (b'error', b'Error')])),
                ('error_message', models.TextField(blank=True)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('parent_id', models.CharField(max_length=255, null=True, blank=True)),
                ('child_id', models.CharField(max_length=255, null=True, blank=True)),
                ('child_volume', models.CharField(max_length=255, null=True, blank=True)),
                ('number_of_aliquot', models.CharField(max_length=255, null=True, blank=True)),
                ('annihilation_date', models.CharField(max_length=255, null=True, blank=True)),
                ('reason', models.CharField(max_length=255, null=True, blank=True)),
                ('panel_type', models.CharField(max_length=255, null=True, blank=True)),
                ('panel_inclusion_criteria', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'cephia_annihilation_row',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'cephia_country',
            },
        ),
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
                ('file_type', models.CharField(max_length=20, choices=[(b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In'), (b'transfer_out', b'Transfer Out'), (b'missing_transfer_out', b'Missing Transfer Out'), (b'annihilation', b'Annihilation')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(default=b'pending', max_length=10, choices=[(b'pending', b'Pending'), (b'imported', b'Imported'), (b'validated', b'Validated'), (b'error', b'Error')])),
                ('priority', models.IntegerField(default=1)),
                ('message', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'cephia_fileinfo',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cephia_location',
            },
        ),
        migrations.CreateModel(
            name='MissingTransferOutRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'processed', b'Processed'), (b'error', b'Error')])),
                ('error_message', models.TextField(blank=True)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('first_aliquot', models.CharField(max_length=255, null=True, blank=True)),
                ('last_aliquot', models.CharField(max_length=255, null=True, blank=True)),
                ('volume', models.CharField(max_length=255, null=True, blank=True)),
                ('aliquots_created', models.CharField(max_length=255, null=True, blank=True)),
                ('panels_used', models.CharField(max_length=255, null=True, blank=True)),
                ('fileinfo', models.ForeignKey(to='cephia.FileInfo')),
            ],
            options={
                'db_table': 'cephia_missing_transfer_out_row',
            },
        ),
        migrations.CreateModel(
            name='PanelInclusionCriteria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cephia_panel_incl_criteria',
            },
        ),
        migrations.CreateModel(
            name='Reason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cephia_reason',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'cephia_region',
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cephia_site',
            },
        ),
        migrations.CreateModel(
            name='Specimen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('specimen_label', models.CharField(max_length=255, null=True, blank=True)),
                ('parent_label', models.CharField(max_length=255, null=True, blank=True)),
                ('num_containers', models.IntegerField(null=True, blank=True)),
                ('reported_draw_date', models.DateField(null=True, blank=True)),
                ('transfer_in_date', models.DateField(null=True, blank=True)),
                ('transfer_out_date', models.DateField(null=True, blank=True)),
                ('created_date', models.DateField(null=True, blank=True)),
                ('modified_date', models.DateField(null=True, blank=True)),
                ('volume', models.FloatField(null=True, blank=True)),
                ('initial_claimed_volume', models.FloatField(null=True, blank=True)),
                ('other_ref', models.CharField(max_length=10, null=True, blank=True)),
                ('aliquoting_reason', models.ForeignKey(blank=True, to='cephia.AliquotingReason', null=True)),
                ('panel_inclusion_criteria', models.ForeignKey(blank=True, to='cephia.PanelInclusionCriteria', null=True)),
                ('reason', models.ForeignKey(blank=True, to='cephia.Reason', null=True)),
            ],
            options={
                'db_table': 'cephia_specimen',
            },
        ),
        migrations.CreateModel(
            name='SpecimenType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('spec_type', models.CharField(max_length=10)),
                ('spec_group', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'cephia_specimen_type',
            },
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cephia_study',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_label', models.CharField(max_length=255, null=True, blank=True)),
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
                ('country', models.ForeignKey(blank=True, to='cephia.Country', null=True)),
                ('ethnicity', models.ForeignKey(blank=True, to='cephia.Ethnicity', null=True)),
            ],
            options={
                'db_table': 'cephia_subject',
            },
        ),
        migrations.CreateModel(
            name='SubjectRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'processed', b'Processed'), (b'error', b'Error')])),
                ('error_message', models.TextField(blank=True)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('subject_label', models.CharField(max_length=255, blank=True)),
                ('source_study', models.CharField(max_length=255, blank=True)),
                ('cohort_entry_date_yyyy', models.CharField(max_length=255, blank=True)),
                ('cohort_entry_date_mm', models.CharField(max_length=255, blank=True)),
                ('cohort_entry_date_dd', models.CharField(max_length=255, blank=True)),
                ('cohort_entry_hiv_status', models.CharField(max_length=255, blank=True)),
                ('country', models.CharField(max_length=255, blank=True)),
                ('last_negative_date_yyyy', models.CharField(max_length=255, blank=True)),
                ('last_negative_date_mm', models.CharField(max_length=255, blank=True)),
                ('last_negative_date_dd', models.CharField(max_length=255, blank=True)),
                ('first_positive_date_yyyy', models.CharField(max_length=255, blank=True)),
                ('first_positive_date_mm', models.CharField(max_length=255, blank=True)),
                ('first_positive_date_dd', models.CharField(max_length=255, blank=True)),
                ('fiebig_stage_at_firstpos', models.CharField(max_length=255, blank=True)),
                ('ars_onset_date_yyyy', models.CharField(max_length=255, blank=True)),
                ('ars_onset_date_mm', models.CharField(max_length=255, blank=True)),
                ('ars_onset_date_dd', models.CharField(max_length=255, blank=True)),
                ('date_of_birth_yyyy', models.CharField(max_length=255, blank=True)),
                ('date_of_birth_mm', models.CharField(max_length=255, blank=True)),
                ('date_of_birth_dd', models.CharField(max_length=255, blank=True)),
                ('sex', models.CharField(max_length=255, blank=True)),
                ('transgender', models.CharField(max_length=255, blank=True)),
                ('population_group', models.CharField(max_length=255, blank=True)),
                ('risk_sex_with_men', models.CharField(max_length=255, blank=True)),
                ('risk_sex_with_women', models.CharField(max_length=255, blank=True)),
                ('risk_idu', models.CharField(max_length=255, blank=True)),
                ('subtype', models.CharField(max_length=255, blank=True)),
                ('subtype_confirmed', models.CharField(max_length=255, blank=True)),
                ('aids_diagnosis_date_yyyy', models.CharField(max_length=255, blank=True)),
                ('aids_diagnosis_date_mm', models.CharField(max_length=255, blank=True)),
                ('aids_diagnosis_date_dd', models.CharField(max_length=255, blank=True)),
                ('art_initiation_date_yyyy', models.CharField(max_length=255, blank=True)),
                ('art_initiation_date_mm', models.CharField(max_length=255, blank=True)),
                ('art_initiation_date_dd', models.CharField(max_length=255, blank=True)),
                ('art_interruption_date_yyyy', models.CharField(max_length=255, blank=True)),
                ('art_interruption_date_mm', models.CharField(max_length=255, blank=True)),
                ('art_interruption_date_dd', models.CharField(max_length=255, blank=True)),
                ('art_resumption_date_yyyy', models.CharField(max_length=255, blank=True)),
                ('art_resumption_date_mm', models.CharField(max_length=255, blank=True)),
                ('art_resumption_date_dd', models.CharField(max_length=255, blank=True)),
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
        migrations.CreateModel(
            name='TransferInRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'processed', b'Processed'), (b'error', b'Error')])),
                ('error_message', models.TextField(blank=True)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('specimen_label', models.CharField(max_length=255, null=True, blank=True)),
                ('subject_label', models.CharField(max_length=255, null=True, blank=True)),
                ('drawdate_year', models.CharField(max_length=255, null=True, blank=True)),
                ('drawdate_month', models.CharField(max_length=255, null=True, blank=True)),
                ('drawdate_day', models.CharField(max_length=255, null=True, blank=True)),
                ('number_of_containers', models.CharField(max_length=255, null=True, blank=True)),
                ('transfer_date_yyyy', models.CharField(max_length=255, null=True, blank=True)),
                ('transfer_date_mm', models.CharField(max_length=255, null=True, blank=True)),
                ('transfer_date_dd', models.CharField(max_length=255, null=True, blank=True)),
                ('receiving_site', models.CharField(max_length=255, null=True, blank=True)),
                ('transfer_reason', models.CharField(max_length=255, null=True, blank=True)),
                ('specimen_type', models.CharField(max_length=255, null=True, blank=True)),
                ('volume', models.CharField(max_length=255, null=True, blank=True)),
                ('volume_units', models.CharField(max_length=255, null=True, blank=True)),
                ('source_study', models.CharField(max_length=255, null=True, blank=True)),
                ('notes', models.CharField(max_length=255, null=True, blank=True)),
                ('visit_linkage', models.CharField(max_length=255, null=True, blank=True)),
                ('fileinfo', models.ForeignKey(to='cephia.FileInfo')),
            ],
            options={
                'db_table': 'cephia_transfer_in_row',
            },
        ),
        migrations.CreateModel(
            name='TransferOutRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'processed', b'Processed'), (b'error', b'Error')])),
                ('error_message', models.TextField(blank=True)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('specimen_label', models.CharField(max_length=255, null=True, blank=True)),
                ('num_containers', models.CharField(max_length=255, null=True, blank=True)),
                ('transfer_out_date', models.CharField(max_length=255, null=True, blank=True)),
                ('to_location', models.CharField(max_length=255, null=True, blank=True)),
                ('transfer_reason', models.CharField(max_length=255, null=True, blank=True)),
                ('spec_type', models.CharField(max_length=255, null=True, blank=True)),
                ('volume', models.CharField(max_length=255, null=True, blank=True)),
                ('other_ref', models.CharField(max_length=255, null=True, blank=True)),
                ('fileinfo', models.ForeignKey(to='cephia.FileInfo')),
            ],
            options={
                'db_table': 'cephia_transfer_out_row',
            },
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_label', models.CharField(max_length=255)),
                ('visit_date', models.DateField(null=True, blank=True)),
                ('status', models.CharField(max_length=8, choices=[(b'negative', b'Negative'), (b'positive', b'Positive'), (b'unknown', b'Unkown')])),
                ('visit_cd4', models.IntegerField(null=True)),
                ('visit_vl', models.CharField(max_length=10, null=True)),
                ('scope_visit_ec', models.CharField(max_length=100, blank=True)),
                ('visit_pregnant', models.NullBooleanField()),
                ('visit_hepatitis', models.NullBooleanField()),
                ('study', models.ForeignKey(blank=True, to='cephia.Study', null=True)),
                ('subject', models.ForeignKey(default=None, blank=True, to='cephia.Subject', null=True)),
            ],
            options={
                'db_table': 'cephia_visit',
            },
        ),
        migrations.CreateModel(
            name='VisitRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'processed', b'Processed'), (b'error', b'Error')])),
                ('error_message', models.TextField(blank=True)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('subject_label', models.CharField(max_length=255, blank=True)),
                ('visitdate_yyyy', models.CharField(max_length=255, blank=True)),
                ('visitdate_mm', models.CharField(max_length=255, blank=True)),
                ('visitdate_dd', models.CharField(max_length=255, blank=True)),
                ('visit_hivstatus', models.CharField(max_length=255, blank=True)),
                ('source_study', models.CharField(max_length=255, blank=True)),
                ('cd4_count', models.CharField(max_length=255, blank=True)),
                ('vl', models.CharField(max_length=255, blank=True)),
                ('scopevisit_ec', models.CharField(max_length=255, blank=True)),
                ('pregnant', models.CharField(max_length=255, blank=True)),
                ('hepatitis', models.CharField(max_length=255, blank=True)),
                ('fileinfo', models.ForeignKey(to='cephia.FileInfo')),
            ],
            options={
                'db_table': 'cephia_visitrow',
            },
        ),
        migrations.AddField(
            model_name='subject',
            name='subtype',
            field=models.ForeignKey(blank=True, to='cephia.Subtype', null=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='source_study',
            field=models.ForeignKey(blank=True, to='cephia.Study', null=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='spec_type',
            field=models.ForeignKey(blank=True, to='cephia.SpecimenType', null=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='subject',
            field=models.ForeignKey(blank=True, to='cephia.Subject', null=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='to_location',
            field=models.ForeignKey(blank=True, to='cephia.Location', null=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='visit',
            field=models.ForeignKey(blank=True, to='cephia.Visit', null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='region',
            field=lib.fields.ProtectedForeignKey(to='cephia.Region', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='annihilationrow',
            name='fileinfo',
            field=models.ForeignKey(to='cephia.FileInfo'),
        ),
    ]
