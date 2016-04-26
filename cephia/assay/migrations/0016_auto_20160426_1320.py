# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0015_auto_20160425_1306'),
    ]

    operations = [
        migrations.RenameField(
            model_name='architectavidityresultrow',
            old_name='treated_SCO',
            new_name='treated_guanidine_SCO',
        ),
        migrations.RenameField(
            model_name='architectavidityresultrow',
            old_name='untreated_SCO',
            new_name='untreated_pbs_SCO',
        ),
    ]
