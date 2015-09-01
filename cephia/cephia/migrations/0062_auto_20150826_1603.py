# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0061_aliquotrow'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TransferReason',
        ),
        migrations.DeleteModel(
            name='Units',
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='file_type',
            field=models.CharField(max_length=20, choices=[(b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In'), (b'transfer_out', b'Transfer Out'), (b'missing_transfer_out', b'Missing Transfer Out'), (b'aliquot', b'Aliquot')]),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='aliquoting_reason',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='AliquotingReason',
        ),
    ]
