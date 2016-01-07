# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0009_auto_20160106_1541'),
    ]

    operations = [
        migrations.RenameField(
            model_name='geeniusresultrow',
            old_name='specimen',
            new_name='blinded_id',
        ),
    ]
