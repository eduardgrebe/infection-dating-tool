# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0041_auto_20150617_2217'),
    ]

    operations = [
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
    ]
