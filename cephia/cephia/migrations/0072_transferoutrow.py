# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0071_auto_20150901_1952'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransferOutRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'validated', b'Validated'), (b'imported', b'Imported'), (b'processed', b'Processed'), (b'error', b'Error')])),
                ('error_message', models.TextField(blank=True)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('specimen_label', models.CharField(max_length=255, null=True, blank=True)),
                ('number_of_containers', models.CharField(max_length=255, null=True, blank=True)),
                ('specimen_type', models.CharField(max_length=255, null=True, blank=True)),
                ('volume', models.CharField(max_length=255, null=True, blank=True)),
                ('volume_units', models.CharField(max_length=255, null=True, blank=True)),
                ('shipped_in_panel', models.CharField(max_length=255, null=True, blank=True)),
                ('shipment_date_dd', models.CharField(max_length=255, null=True, blank=True)),
                ('shipment_date_mm', models.CharField(max_length=255, null=True, blank=True)),
                ('shipment_date_yyyy', models.CharField(max_length=255, null=True, blank=True)),
                ('destination_site', models.CharField(max_length=255, null=True, blank=True)),
                ('comment', models.ForeignKey(to='cephia.ImportedRowComment', null=True)),
                ('fileinfo', models.ForeignKey(to='cephia.FileInfo')),
            ],
            options={
                'db_table': 'cephia_transfer_out_row',
            },
        ),
    ]
