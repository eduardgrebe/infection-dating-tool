# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0009_panel_panelmemberships'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aliquotrow',
            old_name='aliquot_reason',
            new_name='reason',
        ),
    ]
