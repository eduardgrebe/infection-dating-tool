# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0011_auto_20160106_1742'),
    ]

    operations = [
        migrations.RenameField(
            model_name='geeniusresultrow',
            old_name='CTRL',
            new_name='ctrl',
        ),
        migrations.RenameField(
            model_name='geeniusresultrow',
            old_name='gp24',
            new_name='p24',
        ),
        migrations.AddField(
            model_name='geeniusresultrow',
            name='p31',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
