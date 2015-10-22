# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0008_auto_20151022_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='Panel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('volume', models.FloatField(null=True, blank=True)),
                ('specimen_type', models.ForeignKey(to='cephia.SpecimenType', null=True)),
            ],
            options={
                'db_table': 'cephia_panels',
            },
        ),
        migrations.CreateModel(
            name='PanelMemberships',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('replicates', models.IntegerField(null=True, blank=True)),
                ('panel', models.ForeignKey(to='cephia.Panel', null=True)),
                ('visit', models.ForeignKey(to='cephia.Visit', null=True)),
            ],
            options={
                'db_table': 'cephia_panel_memberships',
            },
        ),
    ]
