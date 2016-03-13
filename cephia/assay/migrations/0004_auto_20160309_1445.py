# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0030_auto_20160309_1445'),
        ('assay', '0003_auto_20160225_1413'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lagresult',
            old_name='plate_id',
            new_name='plate_identifier',
        ),
        migrations.RenameField(
            model_name='lagresultrow',
            old_name='assay_kit_lot_id',
            new_name='assay_kit_lot',
        ),
        migrations.RenameField(
            model_name='lagresultrow',
            old_name='site',
            new_name='laboratory',
        ),
        migrations.RenameField(
            model_name='lagresultrow',
            old_name='plate_id',
            new_name='plate_identifier',
        ),
        migrations.RenameField(
            model_name='lagresultrow',
            old_name='specimen',
            new_name='specimen_label',
        ),
        migrations.RemoveField(
            model_name='lagresult',
            name='final_result',
        ),
        migrations.RemoveField(
            model_name='lagresult',
            name='intermediate_1',
        ),
        migrations.RemoveField(
            model_name='lagresult',
            name='intermediate_2',
        ),
        migrations.RemoveField(
            model_name='lagresult',
            name='intermediate_3',
        ),
        migrations.RemoveField(
            model_name='lagresult',
            name='intermediate_4',
        ),
        migrations.RemoveField(
            model_name='lagresult',
            name='intermediate_5',
        ),
        migrations.RemoveField(
            model_name='lagresult',
            name='intermediate_6',
        ),
        migrations.RemoveField(
            model_name='lagresult',
            name='panel_type',
        ),
        migrations.RemoveField(
            model_name='lagresult',
            name='sample_type',
        ),
        migrations.RemoveField(
            model_name='lagresultrow',
            name='final_result',
        ),
        migrations.RemoveField(
            model_name='lagresultrow',
            name='intermediate_1',
        ),
        migrations.RemoveField(
            model_name='lagresultrow',
            name='intermediate_2',
        ),
        migrations.RemoveField(
            model_name='lagresultrow',
            name='intermediate_3',
        ),
        migrations.RemoveField(
            model_name='lagresultrow',
            name='intermediate_4',
        ),
        migrations.RemoveField(
            model_name='lagresultrow',
            name='intermediate_5',
        ),
        migrations.RemoveField(
            model_name='lagresultrow',
            name='intermediate_6',
        ),
        migrations.RemoveField(
            model_name='lagresultrow',
            name='panel_type',
        ),
        migrations.RemoveField(
            model_name='lagresultrow',
            name='sample_type',
        ),
        migrations.AddField(
            model_name='assayresult',
            name='reported_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='assayresult',
            name='visit',
            field=models.ForeignKey(to='cephia.Visit', null=True),
        ),
        migrations.AddField(
            model_name='lagresult',
            name='assay_result',
            field=models.ForeignKey(default=None, to='assay.AssayResult'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lagresult',
            name='result_OD',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='lagresult',
            name='result_ODn',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='lagresult',
            name='result_calibrator_OD',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='lagresult',
            name='specimen_purpose',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='lagresultrow',
            name='result_OD',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='lagresultrow',
            name='result_ODn',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='lagresultrow',
            name='result_calibrator_OD',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='lagresultrow',
            name='specimen_purpose',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
