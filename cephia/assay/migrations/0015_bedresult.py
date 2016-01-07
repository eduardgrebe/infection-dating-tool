# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0019_auto_20160103_2227'),
        ('assay', '0014_auto_20160107_0518'),
    ]

    operations = [
        migrations.CreateModel(
            name='BEDResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sample_type', models.CharField(max_length=255, blank=True)),
                ('test_date', models.DateField(max_length=255, blank=True)),
                ('operator', models.CharField(max_length=255, blank=True)),
                ('assay_kit_lot_id', models.CharField(max_length=255, blank=True)),
                ('plate_id', models.CharField(max_length=255, blank=True)),
                ('test_mode', models.CharField(max_length=255, blank=True)),
                ('well', models.CharField(max_length=255, blank=True)),
                ('intermediate_1', models.CharField(max_length=255, blank=True)),
                ('intermediate_2', models.CharField(max_length=255, blank=True)),
                ('intermediate_3', models.CharField(max_length=255, blank=True)),
                ('intermediate_4', models.CharField(max_length=255, blank=True)),
                ('intermediate_5', models.CharField(max_length=255, blank=True)),
                ('intermediate_6', models.CharField(max_length=255, blank=True)),
                ('final_result', models.CharField(max_length=255, blank=True)),
                ('panel_type', models.CharField(max_length=255, blank=True)),
                ('assay', models.ForeignKey(to='cephia.Assay')),
                ('laboratory', models.ForeignKey(to='cephia.Laboratory', max_length=255, null=True)),
                ('specimen', models.ForeignKey(to='cephia.Specimen')),
            ],
            options={
                'db_table': 'bed_result',
            },
        ),
    ]
