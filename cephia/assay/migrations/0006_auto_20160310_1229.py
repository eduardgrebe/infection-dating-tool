# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0005_remove_assayresult_visit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lagresult',
            old_name='assay_kit_lot_id',
            new_name='assay_kit_lot',
        ),
    ]
