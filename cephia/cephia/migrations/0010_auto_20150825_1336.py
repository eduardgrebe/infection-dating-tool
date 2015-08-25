# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0009_auto_20150825_1333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visit',
            old_name='study',
            new_name='source_study',
        ),
    ]
