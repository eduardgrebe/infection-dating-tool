# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0011_auto_20150825_1342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specimen',
            name='other_ref',
        ),
        migrations.RemoveField(
            model_name='specimen',
            name='panel_inclusion_criteria',
        ),
    ]
