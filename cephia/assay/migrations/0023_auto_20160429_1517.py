# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0022_auto_20160429_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='architectavidityresult',
            name='assay',
            field=models.ForeignKey(to='cephia.Assay', null=True),
        ),
        migrations.AlterField(
            model_name='architectavidityresult',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectavidityresult',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectavidityresult',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectavidityresult',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectavidityresult',
            name='test_date',
            field=models.DateField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectavidityresult',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectavidityresultrow',
            name='assay',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectavidityresultrow',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectavidityresultrow',
            name='laboratory',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectavidityresultrow',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectavidityresultrow',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectavidityresultrow',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectavidityresultrow',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectavidityresultrow',
            name='test_date',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectavidityresultrow',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectunmodifiedresult',
            name='assay',
            field=models.ForeignKey(to='cephia.Assay', null=True),
        ),
        migrations.AlterField(
            model_name='architectunmodifiedresult',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectunmodifiedresult',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectunmodifiedresult',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectunmodifiedresult',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectunmodifiedresult',
            name='test_date',
            field=models.DateField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectunmodifiedresult',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectunmodifiedresultrow',
            name='assay',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectunmodifiedresultrow',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectunmodifiedresultrow',
            name='laboratory',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectunmodifiedresultrow',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectunmodifiedresultrow',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectunmodifiedresultrow',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectunmodifiedresultrow',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectunmodifiedresultrow',
            name='test_date',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='architectunmodifiedresultrow',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bedresult',
            name='assay',
            field=models.ForeignKey(to='cephia.Assay', null=True),
        ),
        migrations.AlterField(
            model_name='bedresult',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bedresult',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bedresult',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bedresult',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bedresult',
            name='test_date',
            field=models.DateField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bedresult',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bedresultrow',
            name='assay',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bedresultrow',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bedresultrow',
            name='laboratory',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bedresultrow',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bedresultrow',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bedresultrow',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bedresultrow',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bedresultrow',
            name='test_date',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bedresultrow',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradaviditycdcresult',
            name='assay',
            field=models.ForeignKey(to='cephia.Assay', null=True),
        ),
        migrations.AlterField(
            model_name='bioradaviditycdcresult',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradaviditycdcresult',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradaviditycdcresult',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradaviditycdcresult',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradaviditycdcresult',
            name='test_date',
            field=models.DateField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradaviditycdcresult',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradaviditycdcresultrow',
            name='assay',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradaviditycdcresultrow',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradaviditycdcresultrow',
            name='laboratory',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradaviditycdcresultrow',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradaviditycdcresultrow',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradaviditycdcresultrow',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradaviditycdcresultrow',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradaviditycdcresultrow',
            name='test_date',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradaviditycdcresultrow',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresult',
            name='assay',
            field=models.ForeignKey(to='cephia.Assay', null=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresult',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresult',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresult',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresult',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresult',
            name='test_date',
            field=models.DateField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresult',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresultrow',
            name='assay',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresultrow',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresultrow',
            name='laboratory',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresultrow',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresultrow',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresultrow',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresultrow',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresultrow',
            name='test_date',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresultrow',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityjhuresult',
            name='assay',
            field=models.ForeignKey(to='cephia.Assay', null=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityjhuresult',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityjhuresult',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityjhuresult',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityjhuresult',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityjhuresult',
            name='test_date',
            field=models.DateField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityjhuresult',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityjhuresultrow',
            name='assay',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityjhuresultrow',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityjhuresultrow',
            name='laboratory',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityjhuresultrow',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityjhuresultrow',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityjhuresultrow',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityjhuresultrow',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityjhuresultrow',
            name='test_date',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityjhuresultrow',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='geeniusresult',
            name='assay',
            field=models.ForeignKey(to='cephia.Assay', null=True),
        ),
        migrations.AlterField(
            model_name='geeniusresult',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='geeniusresult',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='geeniusresult',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='geeniusresult',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='geeniusresult',
            name='test_date',
            field=models.DateField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='geeniusresult',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='geeniusresultrow',
            name='assay',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='geeniusresultrow',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='geeniusresultrow',
            name='laboratory',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='geeniusresultrow',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='geeniusresultrow',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='geeniusresultrow',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='geeniusresultrow',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='geeniusresultrow',
            name='test_date',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='geeniusresultrow',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='idev3result',
            name='assay',
            field=models.ForeignKey(to='cephia.Assay', null=True),
        ),
        migrations.AlterField(
            model_name='idev3result',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='idev3result',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='idev3result',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='idev3result',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='idev3result',
            name='test_date',
            field=models.DateField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='idev3result',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='idev3resultrow',
            name='assay',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='idev3resultrow',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='idev3resultrow',
            name='laboratory',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='idev3resultrow',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='idev3resultrow',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='idev3resultrow',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='idev3resultrow',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='idev3resultrow',
            name='test_date',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='idev3resultrow',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresult',
            name='assay',
            field=models.ForeignKey(to='cephia.Assay', null=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresult',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresult',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresult',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresult',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresult',
            name='test_date',
            field=models.DateField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresult',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresultrow',
            name='assay',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresultrow',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresultrow',
            name='laboratory',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresultrow',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresultrow',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresultrow',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresultrow',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresultrow',
            name='test_date',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresultrow',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresult',
            name='assay',
            field=models.ForeignKey(to='cephia.Assay', null=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresult',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresult',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresult',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresult',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresult',
            name='test_date',
            field=models.DateField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresult',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresultrow',
            name='assay',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresultrow',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresultrow',
            name='laboratory',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresultrow',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresultrow',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresultrow',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresultrow',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresultrow',
            name='test_date',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresultrow',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresult',
            name='assay',
            field=models.ForeignKey(to='cephia.Assay', null=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresult',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresult',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresult',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresult',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresult',
            name='test_date',
            field=models.DateField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresult',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresultrow',
            name='assay',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresultrow',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresultrow',
            name='laboratory',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresultrow',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresultrow',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresultrow',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresultrow',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresultrow',
            name='test_date',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresultrow',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosplasmaresult',
            name='assay',
            field=models.ForeignKey(to='cephia.Assay', null=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosplasmaresult',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosplasmaresult',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosplasmaresult',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosplasmaresult',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosplasmaresult',
            name='test_date',
            field=models.DateField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosplasmaresult',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosplasmaresultrow',
            name='assay',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosplasmaresultrow',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosplasmaresultrow',
            name='laboratory',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosplasmaresultrow',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosplasmaresultrow',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosplasmaresultrow',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosplasmaresultrow',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosplasmaresultrow',
            name='test_date',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosplasmaresultrow',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='luminexcdcresult',
            name='assay',
            field=models.ForeignKey(to='cephia.Assay', null=True),
        ),
        migrations.AlterField(
            model_name='luminexcdcresult',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='luminexcdcresult',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='luminexcdcresult',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='luminexcdcresult',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='luminexcdcresult',
            name='test_date',
            field=models.DateField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='luminexcdcresult',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='luminexcdcresultrow',
            name='assay',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='luminexcdcresultrow',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='luminexcdcresultrow',
            name='laboratory',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='luminexcdcresultrow',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='luminexcdcresultrow',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='luminexcdcresultrow',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='luminexcdcresultrow',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='luminexcdcresultrow',
            name='test_date',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='luminexcdcresultrow',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresult',
            name='assay',
            field=models.ForeignKey(to='cephia.Assay', null=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresult',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresult',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresult',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresult',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresult',
            name='test_date',
            field=models.DateField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresult',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresultrow',
            name='assay',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresultrow',
            name='assay_kit_lot',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresultrow',
            name='laboratory',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresultrow',
            name='operator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresultrow',
            name='plate_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresultrow',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresultrow',
            name='specimen_purpose',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresultrow',
            name='test_date',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresultrow',
            name='test_mode',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
