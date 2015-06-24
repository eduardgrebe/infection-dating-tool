# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0026_auto_20150611_1425'),
    ]

    operations = [
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
                ('fileinfo', models.ForeignKey(to='cephia.FileInfo')),
            ],
            options={
                'db_table': 'cephia_annihilation_row',
            },
        ),
        migrations.CreateModel(
            name='InventoryRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'processed', b'Processed'), (b'error', b'Error')])),
                ('error_message', models.TextField(blank=True)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('original_box_name', models.CharField(max_length=255, null=True, blank=True)),
                ('sample_id', models.CharField(max_length=255, null=True, blank=True)),
                ('draw_date', models.CharField(max_length=255, null=True, blank=True)),
                ('volume', models.CharField(max_length=255, null=True, blank=True)),
                ('box', models.CharField(max_length=255, null=True, blank=True)),
                ('row', models.CharField(max_length=255, null=True, blank=True)),
                ('column', models.CharField(max_length=255, null=True, blank=True)),
                ('comments', models.CharField(max_length=255, null=True, blank=True)),
                ('fileinfo', models.ForeignKey(to='cephia.FileInfo')),
            ],
            options={
                'db_table': 'cephia_inventory_row',
            },
        ),
    ]
