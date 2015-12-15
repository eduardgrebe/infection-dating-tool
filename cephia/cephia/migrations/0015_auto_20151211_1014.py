# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0014_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileinfo',
            name='file_type',
            field=models.CharField(max_length=20, choices=[(b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In'), (b'aliquot', b'Aliquot'), (b'transfer_out', b'Transfer Out'), (b'assay', b'Assay'), (b'panel_shipment', b'Panel Shipment'), (b'panel_membership', b'Panel Membership')]),
        ),
        migrations.AlterField(
            model_name='historicalfileinfo',
            name='file_type',
            field=models.CharField(max_length=20, choices=[(b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In'), (b'aliquot', b'Aliquot'), (b'transfer_out', b'Transfer Out'), (b'assay', b'Assay'), (b'panel_shipment', b'Panel Shipment'), (b'panel_membership', b'Panel Membership')]),
        ),
    ]
