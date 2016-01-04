# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0017_auto_20160101_1452'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assay',
            old_name='short_name',
            new_name='name',
        ),
    ]
