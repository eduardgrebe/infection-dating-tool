# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0019_auto_20160103_2227'),
        ('assay', '0008_auto_20160103_2227'),
    ]

    operations = [
        migrations.CreateModel(
            name='BEDResultRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'validated', b'Validated'), (b'imported', b'Imported'), (b'processed', b'Processed'), (b'error', b'Error')])),
                ('error_message', models.TextField(blank=True)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('specimen', models.CharField(max_length=255, blank=True)),
                ('assay', models.CharField(max_length=255, blank=True)),
                ('sample_type', models.CharField(max_length=255, blank=True)),
                ('site', models.CharField(max_length=255, blank=True)),
                ('test_date', models.CharField(max_length=255, blank=True)),
                ('operator', models.CharField(max_length=255, blank=True)),
                ('assay_kit_lot_id', models.CharField(max_length=255, blank=True)),
                ('plate_id', models.CharField(max_length=255, blank=True)),
                ('test_mode', models.CharField(max_length=255, blank=True)),
                ('well', models.CharField(max_length=255, blank=True)),
                ('intermediate_1', models.CharField(max_length=255, blank=True)),
                ('intermediate_2', models.CharField(max_length=255, blank=True)),
                ('intermediate_3', models.CharField(max_length=255, blank=True)),
                ('intermediate_4', models.CharField(max_length=255, blank=True)),
                ('intermediate_5', models.CharField(max_length=255, blank=True)),
                ('intermediate_6', models.CharField(max_length=255, blank=True)),
                ('final_result', models.CharField(max_length=255, blank=True)),
                ('panel_type', models.CharField(max_length=255, blank=True)),
                ('fileinfo', models.ForeignKey(to='cephia.FileInfo')),
            ],
            options={
                'db_table': 'bed_result_row',
            },
        ),
        migrations.CreateModel(
            name='GeeniusResultRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'validated', b'Validated'), (b'imported', b'Imported'), (b'processed', b'Processed'), (b'error', b'Error')])),
                ('error_message', models.TextField(blank=True)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('specimen', models.CharField(max_length=255, blank=True)),
                ('assay', models.CharField(max_length=255, blank=True)),
                ('sample_type', models.CharField(max_length=255, blank=True)),
                ('site', models.CharField(max_length=255, blank=True)),
                ('test_date', models.CharField(max_length=255, blank=True)),
                ('operator', models.CharField(max_length=255, blank=True)),
                ('assay_kit_lot_id', models.CharField(max_length=255, blank=True)),
                ('plate_id', models.CharField(max_length=255, blank=True)),
                ('test_mode', models.CharField(max_length=255, blank=True)),
                ('well', models.CharField(max_length=255, blank=True)),
                ('gp36', models.CharField(max_length=255, blank=True)),
                ('gp140', models.CharField(max_length=255, blank=True)),
                ('gp160', models.CharField(max_length=255, blank=True)),
                ('gp24', models.CharField(max_length=255, blank=True)),
                ('gp41', models.CharField(max_length=255, blank=True)),
                ('CTRL', models.CharField(max_length=255, blank=True)),
                ('summary', models.CharField(max_length=255, blank=True)),
                ('biorad_confirmatory_result', models.CharField(max_length=255, blank=True)),
                ('panel_type', models.CharField(max_length=255, blank=True)),
                ('exclude', models.CharField(max_length=255, blank=True)),
                ('fileinfo', models.ForeignKey(to='cephia.FileInfo')),
            ],
            options={
                'db_table': 'geenius_result_row',
            },
        ),
        migrations.CreateModel(
            name='LSVitrosResultRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'validated', b'Validated'), (b'imported', b'Imported'), (b'processed', b'Processed'), (b'error', b'Error')])),
                ('error_message', models.TextField(blank=True)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('specimen', models.CharField(max_length=255, blank=True)),
                ('assay', models.CharField(max_length=255, blank=True)),
                ('sample_type', models.CharField(max_length=255, blank=True)),
                ('site', models.CharField(max_length=255, blank=True)),
                ('test_date', models.CharField(max_length=255, blank=True)),
                ('operator', models.CharField(max_length=255, blank=True)),
                ('assay_kit_lot_id', models.CharField(max_length=255, blank=True)),
                ('plate_id', models.CharField(max_length=255, blank=True)),
                ('test_mode', models.CharField(max_length=255, blank=True)),
                ('well', models.CharField(max_length=255, blank=True)),
                ('intermediate_1', models.CharField(max_length=255, blank=True)),
                ('intermediate_2', models.CharField(max_length=255, blank=True)),
                ('intermediate_3', models.CharField(max_length=255, blank=True)),
                ('intermediate_4', models.CharField(max_length=255, blank=True)),
                ('intermediate_5', models.CharField(max_length=255, blank=True)),
                ('intermediate_6', models.CharField(max_length=255, blank=True)),
                ('final_result', models.CharField(max_length=255, blank=True)),
                ('panel_type', models.CharField(max_length=255, blank=True)),
                ('fileinfo', models.ForeignKey(to='cephia.FileInfo')),
            ],
            options={
                'db_table': 'ls_vitros_result_row',
            },
        ),
        migrations.DeleteModel(
            name='ArchitectResult',
        ),
        migrations.DeleteModel(
            name='BioradResult',
        ),
        migrations.DeleteModel(
            name='VitrosResult',
        ),
        migrations.RemoveField(
            model_name='lagresult',
            name='site',
        ),
        migrations.AddField(
            model_name='lagresult',
            name='location',
            field=models.ForeignKey(to='cephia.Location', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='lagresult',
            name='assay',
            field=models.ForeignKey(to='cephia.Assay'),
        ),
        migrations.AlterField(
            model_name='lagresult',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen'),
        ),
        migrations.AlterField(
            model_name='lagresult',
            name='test_date',
            field=models.DateField(max_length=255, blank=True),
        ),
    ]
