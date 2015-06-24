# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0039_remove_specimen_annihilation_date'),
    ]

    operations = [
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
            name='PanelInclusionCriteria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cephia_panel_incl_criteria',
            },
        ),
        migrations.RemoveField(
            model_name='specimen',
            name='aliquoting_reason',
        ),
        migrations.RemoveField(
            model_name='specimen',
            name='panel_inclusion_criteria',
        ),
    ]
