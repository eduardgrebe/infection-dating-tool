# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0007_fileinfo_file_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visitrow',
            old_name='subject',
            new_name='visit_label',
        ),
    ]
