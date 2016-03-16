# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import cephia.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0029_auto_20160314_1341'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('long_name', models.CharField(max_length=255)),
                ('developer', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cephia_assay',
            },
        ),
        migrations.RemoveField(
            model_name='panelmemberships',
            name='panel',
        ),
        migrations.RemoveField(
            model_name='panelmemberships',
            name='visit',
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='panel',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, to='cephia.Panel', null=True),
        ),
        migrations.AddField(
            model_name='historicalfileinfo',
            name='panel',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Panel', null=True),
        ),
        migrations.AddField(
            model_name='panel',
            name='blinded',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='panel',
            name='n_challenge',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='panel',
            name='n_longstanding',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='panel',
            name='n_negative',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='panel',
            name='n_recent',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='panel',
            name='n_reproducibility_controls',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='panel',
            name='n_total',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='panel',
            name='notes',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='panel',
            name='short_name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='file_type',
            field=models.CharField(max_length=20, choices=[(b'', b'---------'), (b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In'), (b'aliquot', b'Aliquot'), (b'transfer_out', b'Transfer Out'), (b'assay', b'Assay'), (b'panel_shipment', b'Panel Shipment'), (b'panel_membership', b'Panel Membership'), (b'diagnostic_test', b'Diagnostic Test'), (b'protocol_lookup', b'Protocol Lookup'), (b'test_history', b'Diagnostic Test History'), (b'test_property', b'Diagnostic Test Properties')]),
        ),
        migrations.AlterField(
            model_name='historicalfileinfo',
            name='file_type',
            field=models.CharField(max_length=20, choices=[(b'', b'---------'), (b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In'), (b'aliquot', b'Aliquot'), (b'transfer_out', b'Transfer Out'), (b'assay', b'Assay'), (b'panel_shipment', b'Panel Shipment'), (b'panel_membership', b'Panel Membership'), (b'diagnostic_test', b'Diagnostic Test'), (b'protocol_lookup', b'Protocol Lookup'), (b'test_history', b'Diagnostic Test History'), (b'test_property', b'Diagnostic Test Properties')]),
        ),
        migrations.AlterField(
            model_name='panel',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.DeleteModel(
            name='PanelMemberships',
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='assay',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, to='cephia.Assay', null=True),
        ),
        migrations.AddField(
            model_name='historicalfileinfo',
            name='assay',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Assay', null=True),
        ),
    ]
