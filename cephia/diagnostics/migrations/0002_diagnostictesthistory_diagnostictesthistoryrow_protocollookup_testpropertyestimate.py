# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0013_auto_20151204_1305'),
        ('diagnostics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiagnosticTestHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test_date', models.DateField(null=True)),
                ('test_result', models.BooleanField()),
                ('subject', models.ForeignKey(to='cephia.Subject', blank=True)),
            ],
            options={
                'db_table': 'diagnostic_test_history',
            },
        ),
        migrations.CreateModel(
            name='DiagnosticTestHistoryRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=255, blank=True)),
                ('test_date', models.CharField(max_length=255, blank=True)),
                ('test_name', models.CharField(max_length=255, blank=True)),
                ('test_result', models.CharField(max_length=255, blank=True)),
                ('source', models.CharField(max_length=255, blank=True)),
                ('protocol', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'db_table': 'diagnostic_test_history_row',
            },
        ),
        migrations.CreateModel(
            name='ProtocolLookup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('protocol', models.CharField(max_length=100)),
                ('test', models.ForeignKey(to='diagnostics.DiagnosticTest')),
            ],
            options={
                'db_table': 'protocol_lookup',
            },
        ),
        migrations.CreateModel(
            name='TestPropertyEstimate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estimate_type', models.CharField(max_length=255, blank=True)),
                ('is_default', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('mean_diagnostic_delay_days', models.IntegerField(null=True)),
                ('diagnostic_test', models.ForeignKey(to='diagnostics.DiagnosticTest', blank=True)),
            ],
            options={
                'db_table': 'test_property_estimates',
            },
        ),
    ]
