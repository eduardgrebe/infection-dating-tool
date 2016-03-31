# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0032_auto_20160315_1552'),
        ('assay', '0003_auto_20160316_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='architectavidityresult',
            name='assay_result',
            field=models.ForeignKey(to='assay.AssayResult', null=True),
        ),
        migrations.AddField(
            model_name='architectavidityresult',
            name='panel',
            field=models.ForeignKey(to='cephia.Panel', null=True),
        ),
        migrations.AddField(
            model_name='architectunmodifiedresult',
            name='assay_result',
            field=models.ForeignKey(to='assay.AssayResult', null=True),
        ),
        migrations.AddField(
            model_name='architectunmodifiedresult',
            name='panel',
            field=models.ForeignKey(to='cephia.Panel', null=True),
        ),
        migrations.AddField(
            model_name='assayresult',
            name='result_unit',
            field=models.CharField(max_length=10, null=True, choices=[(b'ODn', b'Normalised Optical Density'), (b'OD', b'Optical Density'), (b'SCO', b'Signal/Cutoff Ratio'), (b'AI', b'Avidity Index'), (b'GeeniusIndex', b'Geenius Index'), (b'LuminexIndex', b'Luminex Index'), (b'IDEV3Conclusion', b'IDE-V3 Conclusion')]),
        ),
        migrations.AddField(
            model_name='bedresult',
            name='assay_result',
            field=models.ForeignKey(to='assay.AssayResult', null=True),
        ),
        migrations.AddField(
            model_name='bedresult',
            name='panel',
            field=models.ForeignKey(to='cephia.Panel', null=True),
        ),
        migrations.AddField(
            model_name='bioradaviditycdcresult',
            name='assay_result',
            field=models.ForeignKey(to='assay.AssayResult', null=True),
        ),
        migrations.AddField(
            model_name='bioradaviditycdcresult',
            name='panel',
            field=models.ForeignKey(to='cephia.Panel', null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresult',
            name='assay_result',
            field=models.ForeignKey(to='assay.AssayResult', null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresult',
            name='dilution',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresult',
            name='panel',
            field=models.ForeignKey(to='cephia.Panel', null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresult',
            name='result_clasification',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresultrow',
            name='dilution',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresultrow',
            name='result_clasification',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='bioradavidityjhuresult',
            name='assay_result',
            field=models.ForeignKey(to='assay.AssayResult', null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityjhuresult',
            name='panel',
            field=models.ForeignKey(to='cephia.Panel', null=True),
        ),
        migrations.AddField(
            model_name='geeniusresult',
            name='assay_result',
            field=models.ForeignKey(to='assay.AssayResult', null=True),
        ),
        migrations.AddField(
            model_name='geeniusresult',
            name='panel',
            field=models.ForeignKey(to='cephia.Panel', null=True),
        ),
        migrations.AddField(
            model_name='idev3result',
            name='assay_result',
            field=models.ForeignKey(to='assay.AssayResult', null=True),
        ),
        migrations.AddField(
            model_name='idev3result',
            name='panel',
            field=models.ForeignKey(to='cephia.Panel', null=True),
        ),
        migrations.AddField(
            model_name='lagmaximresult',
            name='panel',
            field=models.ForeignKey(to='cephia.Panel', null=True),
        ),
        migrations.AddField(
            model_name='lagsediaresult',
            name='panel',
            field=models.ForeignKey(to='cephia.Panel', null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosdiluentresult',
            name='assay_result',
            field=models.ForeignKey(to='assay.AssayResult', null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosdiluentresult',
            name='panel',
            field=models.ForeignKey(to='cephia.Panel', null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosplasmaresult',
            name='assay_result',
            field=models.ForeignKey(to='assay.AssayResult', null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosplasmaresult',
            name='panel',
            field=models.ForeignKey(to='cephia.Panel', null=True),
        ),
        migrations.AddField(
            model_name='luminexcdcresult',
            name='assay_result',
            field=models.ForeignKey(to='assay.AssayResult', null=True),
        ),
        migrations.AddField(
            model_name='luminexcdcresult',
            name='panel',
            field=models.ForeignKey(to='cephia.Panel', null=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresult',
            name='assay_result',
            field=models.ForeignKey(to='assay.AssayResult', null=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresult',
            name='panel',
            field=models.ForeignKey(to='cephia.Panel', null=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresult',
            name='assay_result',
            field=models.ForeignKey(to='assay.AssayResult', null=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresult',
            name='assay_result',
            field=models.ForeignKey(to='assay.AssayResult', null=True),
        ),
    ]
