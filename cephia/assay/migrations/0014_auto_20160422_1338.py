# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0013_auto_20160422_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='architectavidityresult',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='architectunmodifiedresult',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='bedresult',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='bioradaviditycdcresult',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityglasgowresult',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='bioradavidityjhuresult',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='geeniusresult',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='idev3result',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='lagmaximresult',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='lagsediaresult',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresult',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='lsvitrosplasmaresult',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='luminexcdcresult',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresult',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen', null=True),
        ),
    ]
