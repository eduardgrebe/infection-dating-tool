# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0008_auto_20150825_1125'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visit',
            old_name='status',
            new_name='visit_hivstatus',
        ),
    ]
