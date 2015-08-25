# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0013_auto_20150825_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='AliquotRow',
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
                ('fileinfo', models.ForeignKey(to='cephia.FileInfo')),
            ],
            options={
                'db_table': 'cephia_aliquot_row',
            },
        ),
        migrations.CreateModel(
            name='Units',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cephia_units',
            },
        ),
        migrations.RenameModel(
            old_name='Reason',
            new_name='TransferReason',
        ),
        migrations.RemoveField(
            model_name='annihilationrow',
            name='fileinfo',
        ),
        migrations.DeleteModel(
            name='PanelInclusionCriteria',
        ),
        migrations.RenameField(
            model_name='specimen',
            old_name='num_containers',
            new_name='number_of_containers',
        ),
        migrations.RenameField(
            model_name='specimen',
            old_name='spec_type',
            new_name='specimen_type',
        ),
        migrations.RenameField(
            model_name='specimen',
            old_name='reason',
            new_name='transfer_reason',
        ),
        migrations.RemoveField(
            model_name='specimen',
            name='to_location',
        ),
        migrations.AddField(
            model_name='specimen',
            name='receiving_site',
            field=models.ForeignKey(blank=True, to='cephia.Site', null=True),
        ),
        migrations.AlterModelTable(
            name='transferreason',
            table='cephia_transfer_reason',
        ),
        migrations.DeleteModel(
            name='AnnihilationRow',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.AddField(
            model_name='specimen',
            name='volume_units',
            field=models.ForeignKey(blank=True, to='cephia.Units', null=True),
        ),
    ]
