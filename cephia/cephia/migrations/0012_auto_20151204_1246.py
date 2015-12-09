# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0011_auto_20151102_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsubject',
            name='source_study',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.Study', null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='source_study',
            field=models.ForeignKey(blank=True, to='cephia.Study', null=True),
        ),
    ]
