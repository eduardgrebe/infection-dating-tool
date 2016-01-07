# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0010_auto_20160106_1740'),
    ]

    operations = [
        migrations.RenameField(
            model_name='geeniusresultrow',
            old_name='sample_type',
            new_name='samples',
        ),
    ]
