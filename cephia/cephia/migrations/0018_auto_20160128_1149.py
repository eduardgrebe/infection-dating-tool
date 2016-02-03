# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0017_subjecteddistatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjecteddistatus',
            name='status',
            field=models.CharField(max_length=30, null=True, choices=[(b'ok', b'OK'), (b'investigate', b'Investigate'), (b'suspected_incorrect_data', b'Suspected Incorrect Data'), (b'other', b'Other')]),
        ),
    ]
