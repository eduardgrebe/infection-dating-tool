# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-17 09:22
from __future__ import unicode_literals

import cephia.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0068_merge'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('outside_eddi', '0019_auto_20161014_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalOutsideEddiProtocolLookup',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('protocol', models.CharField(max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('test', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='outside_eddi.OutsideEddiDiagnosticTest')),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical outside eddi protocol lookup',
            },
        ),
        migrations.CreateModel(
            name='OutsideEddiDiagnosticTestHistoryRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[(b'recalled', b'Recalled'), (b'pending', b'Pending'), (b'validated', b'Validated'), (b'imported', b'Imported'), (b'processed', b'Processed'), (b'error', b'Error')], max_length=20)),
                ('error_message', models.TextField(blank=True)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(blank=True, max_length=255)),
                ('test_date', models.CharField(blank=True, max_length=255)),
                ('test_code', models.CharField(blank=True, max_length=255)),
                ('test_result', models.CharField(blank=True, max_length=255)),
                ('source', models.CharField(blank=True, max_length=255)),
                ('protocol', models.CharField(blank=True, max_length=255)),
                ('fileinfo', cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cephia.FileInfo')),
                ('test_history', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='outside_eddi.OutsideEddiDiagnosticTestHistory')),
            ],
            options={
                'db_table': 'outside_eddi_cephia_diagnostic_test_history_row',
            },
        ),
        migrations.CreateModel(
            name='OutsideEddiProtocolLookup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('protocol', models.CharField(max_length=100)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='outside_eddi.OutsideEddiDiagnosticTest')),
            ],
            options={
                'db_table': 'outside_eddi_cephia_protocol_lookup',
            },
        ),
    ]
