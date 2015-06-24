# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0027_annihilationrow_inventoryrow'),
    ]

    operations = [
        migrations.AddField(
            model_name='specimen',
            name='transfer_out_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='file_type',
            field=models.CharField(max_length=20, choices=[(b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In'), (b'transfer_out', b'Transfer Out'), (b'missing_transfer_out', b'Missing Transfer Out'), (b'annihilation', b'Annihilation'), (b'inventory', b'Inventory')]),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='initial_claimed_volume',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='reason',
            field=models.ForeignKey(blank=True, to='cephia.Reason', null=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='reported_draw_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='source_study',
            field=models.ForeignKey(blank=True, to='cephia.Study', null=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='spec_type',
            field=models.ForeignKey(blank=True, to='cephia.SpecimenType', null=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='volume',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
