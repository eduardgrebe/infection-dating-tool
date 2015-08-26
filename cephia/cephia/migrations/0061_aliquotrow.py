# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0060_auto_20150826_1103'),
    ]

    operations = [
        migrations.CreateModel(
            name='AliquotRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'processed', b'Processed'), (b'error', b'Error')])),
                ('error_message', models.TextField(blank=True)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('parent_label', models.CharField(max_length=255, null=True, blank=True)),
                ('aliquot_label', models.CharField(max_length=255, null=True, blank=True)),
                ('volume', models.CharField(max_length=255, null=True, blank=True)),
                ('volume_units', models.CharField(max_length=255, null=True, blank=True)),
                ('number_of_aliquot', models.CharField(max_length=255, null=True, blank=True)),
                ('aliquoting_date_yyyy', models.CharField(max_length=255, null=True, blank=True)),
                ('aliquoting_date_mm', models.CharField(max_length=255, null=True, blank=True)),
                ('aliquoting_date_dd', models.CharField(max_length=255, null=True, blank=True)),
                ('aliquot_reason', models.CharField(max_length=255, null=True, blank=True)),
                ('fileinfo', models.ForeignKey(to='cephia.FileInfo')),
            ],
            options={
                'db_table': 'cephia_aliquot_row',
            },
        ),
    ]
