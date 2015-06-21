# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0044_auto_20150619_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryrow',
            name='fileinfo',
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='file_type',
            field=models.CharField(max_length=20, choices=[(b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In'), (b'transfer_out', b'Transfer Out'), (b'missing_transfer_out', b'Missing Transfer Out'), (b'annihilation', b'Annihilation')]),
        ),
        migrations.DeleteModel(
            name='InventoryRow',
        ),
    ]
