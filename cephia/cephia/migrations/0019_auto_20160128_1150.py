# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0018_auto_20160128_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsubject',
            name='subject_eddi_status',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.SubjectEDDIStatus', null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='subject_eddi_status',
            field=models.ForeignKey(blank=True, to='cephia.SubjectEDDIStatus', null=True),
        ),
    ]
