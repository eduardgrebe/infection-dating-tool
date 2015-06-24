# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0012_specimentype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cephia_location',
            },
        ),
        migrations.CreateModel(
            name='Reason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cephia_reason',
            },
        ),
        migrations.CreateModel(
            name='Specimen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('num_containers', models.IntegerField(default=1)),
                ('reported_draw_date', models.DateField()),
                ('transfer_in_date', models.DateField()),
                ('volume', models.IntegerField()),
                ('initial_claimed_volume', models.IntegerField()),
                ('other_ref', models.IntegerField()),
                ('site', models.CharField(max_length=5, choices=[(b'BSRI', b'BSRI'), (b'PHE', b'PHE')])),
                ('reason', models.ForeignKey(to='cephia.Reason')),
            ],
            options={
                'db_table': 'cephia_specimen',
            },
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cephia_study',
            },
        ),
        migrations.CreateModel(
            name='TransferInRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('specimen_label', models.CharField(max_length=255)),
                ('patient_label', models.CharField(max_length=255, null=True)),
                ('draw_date', models.CharField(max_length=255, null=True)),
                ('num_containers', models.CharField(max_length=255)),
                ('transfer_in_date', models.CharField(max_length=255, null=True, blank=True)),
                ('sites', models.CharField(max_length=255)),
                ('transfer_reason', models.CharField(max_length=255)),
                ('spec_type', models.CharField(max_length=255)),
                ('volume', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cephia_transfer_in_row',
            },
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='file_type',
            field=models.CharField(max_length=20, choices=[(b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In')]),
        ),
        migrations.AddField(
            model_name='specimen',
            name='source_study',
            field=models.ForeignKey(to='cephia.Study'),
        ),
        migrations.AddField(
            model_name='specimen',
            name='spec_type',
            field=models.ForeignKey(to='cephia.SpecimenType'),
        ),
        migrations.AddField(
            model_name='specimen',
            name='to_location',
            field=models.ForeignKey(to='cephia.Location'),
        ),
    ]
