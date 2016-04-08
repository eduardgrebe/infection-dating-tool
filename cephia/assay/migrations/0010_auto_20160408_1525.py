# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0009_auto_20160408_1259'),
    ]

    operations = [
        migrations.RenameField(
            model_name='architectavidityresult',
            old_name='AI_recalc',
            new_name='AI_reported',
        ),
        migrations.RenameField(
            model_name='architectavidityresultrow',
            old_name='AI_recalc',
            new_name='AI_reported',
        ),
        migrations.RemoveField(
            model_name='architectavidityresultrow',
            name='SCO',
        ),
    ]
