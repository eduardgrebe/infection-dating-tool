# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0032_auto_20160315_1552'),
        ('assay', '0002_auto_20160406_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='architectavidityresult',
            name='laboratory',
            field=models.ForeignKey(to='cephia.Laboratory', null=True),
        ),
        migrations.AddField(
            model_name='architectunmodifiedresult',
            name='laboratory',
            field=models.ForeignKey(to='cephia.Laboratory', null=True),
        ),
        migrations.AddField(
            model_name='bedresult',
            name='laboratory',
            field=models.ForeignKey(to='cephia.Laboratory', null=True),
        ),
        migrations.AddField(
            model_name='bioradaviditycdcresult',
            name='laboratory',
            field=models.ForeignKey(to='cephia.Laboratory', null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresult',
            name='laboratory',
            field=models.ForeignKey(to='cephia.Laboratory', null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityjhuresult',
            name='laboratory',
            field=models.ForeignKey(to='cephia.Laboratory', null=True),
        ),
        migrations.AddField(
            model_name='geeniusresult',
            name='laboratory',
            field=models.ForeignKey(to='cephia.Laboratory', null=True),
        ),
        migrations.AddField(
            model_name='idev3result',
            name='laboratory',
            field=models.ForeignKey(to='cephia.Laboratory', null=True),
        ),
        migrations.AddField(
            model_name='lagmaximresult',
            name='laboratory',
            field=models.ForeignKey(to='cephia.Laboratory', null=True),
        ),
        migrations.AddField(
            model_name='lagsediaresult',
            name='laboratory',
            field=models.ForeignKey(to='cephia.Laboratory', null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosdiluentresult',
            name='laboratory',
            field=models.ForeignKey(to='cephia.Laboratory', null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosplasmaresult',
            name='laboratory',
            field=models.ForeignKey(to='cephia.Laboratory', null=True),
        ),
        migrations.AddField(
            model_name='luminexcdcresult',
            name='laboratory',
            field=models.ForeignKey(to='cephia.Laboratory', null=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresult',
            name='laboratory',
            field=models.ForeignKey(to='cephia.Laboratory', null=True),
        ),
    ]
