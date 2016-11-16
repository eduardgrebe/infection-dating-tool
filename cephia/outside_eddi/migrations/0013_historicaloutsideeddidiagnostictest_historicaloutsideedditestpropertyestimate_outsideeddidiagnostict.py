# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-06 08:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import lib.fields


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0021_historicaldiagnostictest_historicaldiagnostictesthistory_historicalprotocollookup_historicaltestprop'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('outside_eddi', '0012_auto_20161005_1019'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalOutsideEddiDiagnosticTest',
            fields=[
                ('id', models.IntegerField(db_index=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical outside eddi diagnostic test',
            },
        ),
        migrations.CreateModel(
            name='HistoricalOutsideEddiTestPropertyEstimate',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('active_property', models.BooleanField(default=False)),
                ('estimate_label', models.CharField(blank=True, max_length=255)),
                ('estimate_type', models.CharField(blank=True, max_length=255)),
                ('mean_diagnostic_delay_days', models.IntegerField(null=True)),
                ('diagnostic_delay_median', models.IntegerField(null=True)),
                ('foursigma_diagnostic_delay_days', models.IntegerField(null=True)),
                ('is_default', models.BooleanField(default=False)),
                ('time0_ref', models.CharField(blank=True, max_length=255)),
                ('comment', models.CharField(blank=True, max_length=255)),
                ('reference', models.CharField(blank=True, max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('test', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='diagnostics.DiagnosticTest')),
                ('user', lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical outside eddi test property estimate',
            },
        ),
        migrations.CreateModel(
            name='OutsideEddiDiagnosticTest',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'outside_eddi_diagnostic_tests',
            },
        ),
        migrations.CreateModel(
            name='OutsideEddiTestPropertyEstimate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_property', models.BooleanField(default=False)),
                ('estimate_label', models.CharField(blank=True, max_length=255)),
                ('estimate_type', models.CharField(blank=True, max_length=255)),
                ('mean_diagnostic_delay_days', models.IntegerField(null=True)),
                ('diagnostic_delay_median', models.IntegerField(null=True)),
                ('foursigma_diagnostic_delay_days', models.IntegerField(null=True)),
                ('is_default', models.BooleanField(default=False)),
                ('time0_ref', models.CharField(blank=True, max_length=255)),
                ('comment', models.CharField(blank=True, max_length=255)),
                ('reference', models.CharField(blank=True, max_length=255)),
                ('test', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='diagnostics.DiagnosticTest')),
                ('user', lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'outside_eddi_test_property_estimates',
            },
        ),
    ]