# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0029_auto_20160314_1341'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subjecteddi',
            old_name='tci_begin',
            new_name='ep_ddi',
        ),
        migrations.RenameField(
            model_name='subjecteddi',
            old_name='tci_size',
            new_name='interval_size',
        ),
        migrations.RenameField(
            model_name='subjecteddi',
            old_name='tci_end',
            new_name='lp_ddi',
        ),
        migrations.RemoveField(
            model_name='visiteddi',
            name='eddi',
        ),
        migrations.RemoveField(
            model_name='visiteddi',
            name='tci_begin',
        ),
        migrations.RemoveField(
            model_name='visiteddi',
            name='tci_end',
        ),
        migrations.AddField(
            model_name='visiteddi',
            name='days_since_eddi',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='visiteddi',
            name='days_since_ep_ddi',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='visiteddi',
            name='days_since_lp_ddi',
            field=models.IntegerField(null=True),
        ),
    ]
