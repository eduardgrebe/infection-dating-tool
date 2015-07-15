# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0054_auto_20150715_1124'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visit',
            old_name='visit_label',
            new_name='patient_label',
        ),
        migrations.RenameField(
            model_name='visitrow',
            old_name='visit_label',
            new_name='patient_label',
        ),
    ]
