# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0006_auto_20160407_1502'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bioradavidityglasgowresult',
            old_name='clasification',
            new_name='classification',
        ),
        migrations.RenameField(
            model_name='bioradavidityglasgowresultrow',
            old_name='clasification',
            new_name='classification',
        ),
    ]
