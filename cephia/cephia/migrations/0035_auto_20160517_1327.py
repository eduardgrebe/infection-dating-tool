# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0034_auto_20160511_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalvisit',
            name='days_on_art',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='historicalvisit',
            name='first_treatment',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='historicalvisit',
            name='vl_detectable',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='visit',
            name='days_on_art',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='first_treatment',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='visit',
            name='vl_detectable',
            field=models.NullBooleanField(),
        ),
    ]
