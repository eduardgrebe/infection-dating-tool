# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0083_aliquotrow_specimen_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cephia_locations',
            },
        ),
        migrations.RenameModel(
            old_name='Site',
            new_name='Laboratory',
        ),
        migrations.RenameField(
            model_name='historicalspecimen',
            old_name='receiving_site',
            new_name='laboratory',
        ),
        migrations.RenameField(
            model_name='specimen',
            old_name='receiving_site',
            new_name='laboratory',
        ),
        migrations.AlterModelTable(
            name='aliquotrow',
            table='cephia_aliquot_rows',
        ),
        migrations.AlterModelTable(
            name='cephiauser',
            table='cephia_users',
        ),
        migrations.AlterModelTable(
            name='country',
            table='cephia_countries',
        ),
        migrations.AlterModelTable(
            name='ethnicity',
            table='cephia_ethnicities',
        ),
        migrations.AlterModelTable(
            name='fileinfo',
            table='cephia_datafiles',
        ),
        migrations.AlterModelTable(
            name='importedrowcomment',
            table='cephia_importedrow_comments',
        ),
        migrations.AlterModelTable(
            name='laboratory',
            table='cephia_laboratories',
        ),
        migrations.AlterModelTable(
            name='region',
            table='cephia_regions',
        ),
        migrations.AlterModelTable(
            name='specimen',
            table='cephia_specimens',
        ),
        migrations.AlterModelTable(
            name='specimentype',
            table='cephia_specimen_types',
        ),
        migrations.AlterModelTable(
            name='study',
            table='cephia_studies',
        ),
        migrations.AlterModelTable(
            name='subject',
            table='cephia_subjects',
        ),
        migrations.AlterModelTable(
            name='subjectrow',
            table='cephia_subjectrows',
        ),
        migrations.AlterModelTable(
            name='subtype',
            table='cephia_subtypes',
        ),
        migrations.AlterModelTable(
            name='transferinrow',
            table='cephia_transfer_in_rows',
        ),
        migrations.AlterModelTable(
            name='transferoutrow',
            table='cephia_transfer_out_rows',
        ),
        migrations.AlterModelTable(
            name='visit',
            table='cephia_visits',
        ),
        migrations.AlterModelTable(
            name='visitrow',
            table='cephia_visitrows',
        ),
        migrations.AddField(
            model_name='historicalspecimen',
            name='shipped_to',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.Location', null=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='shipped_to',
            field=models.ForeignKey(blank=True, to='cephia.Location', null=True),
        ),
    ]
