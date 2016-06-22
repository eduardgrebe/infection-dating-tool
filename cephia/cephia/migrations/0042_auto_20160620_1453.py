# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-20 12:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import lib.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0041_auto_20160609_0957'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('after_aids_diagnosis', models.NullBooleanField()),
                ('age_in_years', models.PositiveIntegerField(null=True)),
                ('ever_aids_diagnosis', models.NullBooleanField()),
                ('ever_scope_ec', models.NullBooleanField()),
                ('earliest_visit_date', models.DateTimeField(null=True)),
                ('days_since_cohort_entry', models.PositiveIntegerField(null=True)),
                ('days_since_first_draw', models.PositiveIntegerField(null=True)),
                ('days_since_first_art_visit', models.PositiveIntegerField(null=True)),
                ('days_from_eddi_to_first_art', models.PositiveIntegerField(null=True)),
                ('days_from_eddi_to_current_art', models.PositiveIntegerField(null=True)),
                ('region', models.CharField(max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='historicalvisit',
            name='days_on_art',
        ),
        migrations.RemoveField(
            model_name='visit',
            name='days_on_art',
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='file_type',
            field=models.CharField(choices=[(b'', b'---------'), (b'aliquot', b'Aliquot'), (b'assay', b'Assay'), (b'diagnostic_test', b'Diagnostic Test'), (b'panel_shipment', b'Panel Shipment'), (b'panel_membership', b'Panel Membership'), (b'protocol_lookup', b'Protocol Lookup'), (b'subject', b'Subject'), (b'test_history', b'Diagnostic Test History'), (b'test_property', b'Diagnostic Test Properties'), (b'transfer_in', b'Transfer In'), (b'transfer_out', b'Transfer Out'), (b'visit', b'Visit')], max_length=20),
        ),
        migrations.AlterField(
            model_name='historicalfileinfo',
            name='file_type',
            field=models.CharField(choices=[(b'', b'---------'), (b'aliquot', b'Aliquot'), (b'assay', b'Assay'), (b'diagnostic_test', b'Diagnostic Test'), (b'panel_shipment', b'Panel Shipment'), (b'panel_membership', b'Panel Membership'), (b'protocol_lookup', b'Protocol Lookup'), (b'subject', b'Subject'), (b'test_history', b'Diagnostic Test History'), (b'test_property', b'Diagnostic Test Properties'), (b'transfer_in', b'Transfer In'), (b'transfer_out', b'Transfer Out'), (b'visit', b'Visit')], max_length=20),
        ),
        migrations.AddField(
            model_name='visitdetail',
            name='visit',
            field=lib.fields.OneToOneOrNoneField(on_delete=django.db.models.deletion.CASCADE, related_name='visitdetail', to='cephia.Visit'),
        ),
    ]