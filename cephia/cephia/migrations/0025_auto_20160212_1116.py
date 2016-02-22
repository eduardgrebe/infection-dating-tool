# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0024_subjecteddi_recalculate'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalvisit',
            name='on_treatment',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='historicalvisit',
            name='treatment_naive',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='visit',
            name='on_treatment',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='visit',
            name='treatment_naive',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='subjecteddistatus',
            name='status',
            field=models.CharField(max_length=30, null=True, choices=[(b'ok', b'OK'), (b'investigate', b'Investigate'), (b'suspected_incorrect_data', b'Suspected Incorrect Data'), (b'resolved', b'Resolved'), (b'other', b'Other')]),
        ),
    ]
