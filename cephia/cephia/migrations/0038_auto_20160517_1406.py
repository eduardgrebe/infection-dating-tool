# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0037_auto_20160517_1345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalvisit',
            old_name='vl',
            new_name='vl_reported',
        ),
        migrations.RenameField(
            model_name='visit',
            old_name='vl',
            new_name='vl_reported',
        ),
        migrations.AddField(
            model_name='historicalvisit',
            name='viral_load',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='historicalvisit',
            name='vl_type',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='viral_load',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='vl_type',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
