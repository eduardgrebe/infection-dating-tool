# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0005_auto_20150607_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'cephia_source',
            },
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visit_date', models.DateField(null=True, blank=True)),
                ('status', models.CharField(max_length=8, choices=[(b'negative', b'Negative'), (b'positive', b'Positive'), (b'unknown', b'Unkown')])),
                ('visit_cd4', models.IntegerField()),
                ('visit_vl', models.CharField(max_length=10, blank=True)),
                ('scope_visit_ec', models.CharField(max_length=100, blank=True)),
                ('visit_pregnant', models.NullBooleanField()),
                ('visit_hepatitis', models.NullBooleanField()),
                ('source', models.ForeignKey(to='cephia.Source')),
                ('subject', models.ForeignKey(to='cephia.Subject')),
            ],
            options={
                'db_table': 'cephia_visit',
            },
        ),
        migrations.CreateModel(
            name='VisitRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=9, choices=[(b'pending', b'Pending'), (b'processed', b'Processed'), (b'error', b'Error')])),
                ('error_message', models.TextField(blank=True)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(max_length=255, blank=True)),
                ('visit_date', models.CharField(max_length=255, blank=True)),
                ('status', models.CharField(max_length=255, blank=True)),
                ('source', models.CharField(max_length=255, blank=True)),
                ('visit_cd4', models.CharField(max_length=255, blank=True)),
                ('visit_vl', models.CharField(max_length=255, blank=True)),
                ('scope_visit_ec', models.CharField(max_length=255, blank=True)),
                ('visit_pregnant', models.CharField(max_length=255, blank=True)),
                ('visit_hepatitis', models.CharField(max_length=255, blank=True)),
                ('fileinfo', models.ForeignKey(to='cephia.FileInfo')),
            ],
            options={
                'db_table': 'cephia_visitrow',
            },
        ),
    ]
