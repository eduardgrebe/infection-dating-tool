# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0007_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='ars_onset',
            new_name='ars_onset_date',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='anti_retroviral_initiation_date',
            new_name='art_initiation_date',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='treatment_interruption_date',
            new_name='art_interruption_date',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='treatment_resumption_date',
            new_name='art_resumption_date',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='entry_date',
            new_name='cohort_entry_date',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='entry_status',
            new_name='cohort_entry_hiv_status',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='dob',
            new_name='date_of_birth',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='fiebig',
            new_name='fiebig_stage_at_firstpos',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='last_positive_date',
            new_name='first_positive_date',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='ethnicity',
            new_name='population_group',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='iv_drug_user',
            new_name='risk_idu',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='sex_with_men',
            new_name='risk_sex_with_men',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='sex_with_women',
            new_name='risk_sex_with_women',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='gender',
            new_name='sex',
        ),
        migrations.AddField(
            model_name='subject',
            name='date_of_death',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='transgender',
            field=models.NullBooleanField(),
        ),
    ]
