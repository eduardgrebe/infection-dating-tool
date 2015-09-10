# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0075_auto_20150909_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalspecimen',
            name='provisional_visit',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.Visit', null=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='provisional_visit',
            field=models.ForeignKey(related_name='provisional_visit', to='cephia.Visit', null=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='subject',
            field=models.ForeignKey(to='cephia.Subject', null=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='visit',
            field=models.ForeignKey(related_name='visit', to='cephia.Visit', null=True),
        ),
    ]
