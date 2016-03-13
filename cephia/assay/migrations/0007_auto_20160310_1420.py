# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0030_auto_20160309_1445'),
        ('assay', '0006_auto_20160310_1229'),
    ]

    operations = [
        migrations.CreateModel(
            name='LSVitrosResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operator', models.CharField(max_length=255, blank=True)),
                ('assay_kit_lot', models.CharField(max_length=255, blank=True)),
                ('plate_identifier', models.CharField(max_length=255, blank=True)),
                ('well', models.CharField(max_length=255, blank=True)),
                ('test_mode', models.CharField(max_length=255, blank=True)),
                ('specimen_purpose', models.CharField(max_length=255, blank=True)),
                ('result_SCO', models.FloatField(max_length=255, blank=True)),
                ('panel_type', models.CharField(max_length=255, blank=True)),
                ('test_date', models.DateField(max_length=255, blank=True)),
                ('assay', models.ForeignKey(to='cephia.Assay')),
                ('assay_result', models.ForeignKey(to='assay.AssayResult')),
                ('laboratory', models.ForeignKey(to='cephia.Laboratory', max_length=255, null=True)),
                ('specimen', models.ForeignKey(to='cephia.Specimen')),
            ],
            options={
                'db_table': 'ls_vitros_result',
            },
        ),
        migrations.RenameField(
            model_name='lsvitrosresultrow',
            old_name='assay_kit_lot_id',
            new_name='assay_kit_lot',
        ),
        migrations.RemoveField(
            model_name='lsvitrosresultrow',
            name='final_result',
        ),
        migrations.RemoveField(
            model_name='lsvitrosresultrow',
            name='intermediate_1',
        ),
        migrations.RemoveField(
            model_name='lsvitrosresultrow',
            name='intermediate_2',
        ),
        migrations.RemoveField(
            model_name='lsvitrosresultrow',
            name='intermediate_3',
        ),
        migrations.RemoveField(
            model_name='lsvitrosresultrow',
            name='intermediate_4',
        ),
        migrations.RemoveField(
            model_name='lsvitrosresultrow',
            name='intermediate_5',
        ),
        migrations.RemoveField(
            model_name='lsvitrosresultrow',
            name='intermediate_6',
        ),
        migrations.RemoveField(
            model_name='lsvitrosresultrow',
            name='plate_id',
        ),
        migrations.RemoveField(
            model_name='lsvitrosresultrow',
            name='sample_type',
        ),
        migrations.RemoveField(
            model_name='lsvitrosresultrow',
            name='site',
        ),
        migrations.RemoveField(
            model_name='lsvitrosresultrow',
            name='specimen',
        ),
        migrations.AddField(
            model_name='lsvitrosresultrow',
            name='laboratory',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='lsvitrosresultrow',
            name='plate_identifier',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='lsvitrosresultrow',
            name='result_SCO',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='lsvitrosresultrow',
            name='specimen_label',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='lsvitrosresultrow',
            name='specimen_purpose',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
