# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0032_auto_20160315_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalvisit',
            name='on_treatment',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='historicalvisit',
            name='treatment_naive',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='visit',
            name='on_treatment',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='visit',
            name='treatment_naive',
            field=models.BooleanField(default=False),
        ),
    ]