# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0003_auto_20150821_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalspecimen',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='specimen',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='transferinrow',
            name='receiving_site',
        ),
        migrations.AddField(
            model_name='historicalspecimen',
            name='location',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.Location', null=True),
        ),
        migrations.AddField(
            model_name='historicalspecimen',
            name='parent',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.Specimen', null=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='location',
            field=models.ForeignKey(blank=True, to='cephia.Location', null=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='parent',
            field=models.ForeignKey(default=None, to='cephia.Specimen', null=True),
        ),
        migrations.AddField(
            model_name='transferinrow',
            name='location',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalspecimen',
            name='created_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalspecimen',
            name='shipped_to',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.Laboratory', null=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='created_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='shipped_to',
            field=models.ForeignKey(related_name='shipped_to', blank=True, to='cephia.Laboratory', null=True),
        ),
    ]
