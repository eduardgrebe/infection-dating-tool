# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0013_auto_20151204_1305'),
        ('diagnostics', '0003_auto_20160112_2057'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiagnosticTestHistoryRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'validated', b'Validated'), (b'imported', b'Imported'), (b'processed', b'Processed'), (b'error', b'Error')])),
                ('error_message', models.TextField(blank=True)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(max_length=255, blank=True)),
                ('test_date', models.CharField(max_length=255, blank=True)),
                ('test_name', models.CharField(max_length=255, blank=True)),
                ('test_result', models.CharField(max_length=255, blank=True)),
                ('source', models.CharField(max_length=255, blank=True)),
                ('protocol', models.CharField(max_length=255, blank=True)),
                ('fileinfo', models.ForeignKey(to='cephia.FileInfo')),
            ],
            options={
                'db_table': 'diagnostic_test_history_row',
            },
        ),
    ]
