# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0002_auto_20150823_1754'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='patient_label',
            new_name='subject_label',
        ),
    ]
