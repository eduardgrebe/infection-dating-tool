# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0014_auto_20160113_0437'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectEDDI',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tci_begin', models.DateField(null=True, blank=True)),
                ('tci_end', models.DateField(null=True, blank=True)),
                ('eddi', models.DateField(null=True, blank=True)),
            ],
            options={
                'db_table': 'cephia_subject_eddi',
            },
        ),
        migrations.CreateModel(
            name='VisitEDDI',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tci_begin', models.DateField(null=True, blank=True)),
                ('tci_end', models.DateField(null=True, blank=True)),
                ('eddi', models.DateField(null=True, blank=True)),
            ],
            options={
                'db_table': 'cephia_visit_eddi',
            },
        ),
        migrations.RemoveField(
            model_name='historicalsubject',
            name='eddi_max',
        ),
        migrations.RemoveField(
            model_name='historicalsubject',
            name='eddi_mid_point_estimate',
        ),
        migrations.RemoveField(
            model_name='historicalsubject',
            name='eddi_min',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='eddi_max',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='eddi_mid_point_estimate',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='eddi_min',
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='file_type',
            field=models.CharField(max_length=20, choices=[(b'', b'---------'), (b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In'), (b'aliquot', b'Aliquot'), (b'transfer_out', b'Transfer Out'), (b'diagnostic_test', b'Diagnostic Test'), (b'protocol_lookup', b'Protocol Lookup'), (b'diagnostic_test_history', b'Diagnostic Test History')]),
        ),
        migrations.AlterField(
            model_name='historicalfileinfo',
            name='file_type',
            field=models.CharField(max_length=20, choices=[(b'', b'---------'), (b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In'), (b'aliquot', b'Aliquot'), (b'transfer_out', b'Transfer Out'), (b'diagnostic_test', b'Diagnostic Test'), (b'protocol_lookup', b'Protocol Lookup'), (b'diagnostic_test_history', b'Diagnostic Test History')]),
        ),
        migrations.AddField(
            model_name='historicalsubject',
            name='subject_eddi',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.SubjectEDDI', null=True),
        ),
        migrations.AddField(
            model_name='historicalvisit',
            name='visit_eddi',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.VisitEDDI', null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='subject_eddi',
            field=models.ForeignKey(blank=True, to='cephia.SubjectEDDI', null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='visit_eddi',
            field=models.ForeignKey(blank=True, to='cephia.VisitEDDI', null=True),
        ),
    ]
