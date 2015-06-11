# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0024_remove_specimen_to_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransferOutRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'processed', b'Processed'), (b'error', b'Error')])),
                ('error_message', models.TextField(blank=True)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('specimen_label', models.CharField(max_length=255, blank=True)),
                ('num_containers', models.CharField(max_length=255, blank=True)),
                ('transfer_out_date', models.CharField(max_length=255, null=True, blank=True)),
                ('to_location', models.CharField(max_length=255, blank=True)),
                ('transfer_reason', models.CharField(max_length=255, blank=True)),
                ('spec_type', models.CharField(max_length=255, blank=True)),
                ('volume', models.CharField(max_length=255, blank=True)),
                ('other_ref', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'db_table': 'cephia_transfer_out_row',
            },
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='file_type',
            field=models.CharField(max_length=20, choices=[(b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In'), (b'transfer_out', b'Transfer Out'), (b'missing_transfer_out', b'Missing Transfer Out'), (b'annihilation', b'Annihaltion'), (b'inventory', b'Inventory')]),
        ),
        migrations.AddField(
            model_name='transferoutrow',
            name='fileinfo',
            field=models.ForeignKey(to='cephia.FileInfo'),
        ),
    ]
