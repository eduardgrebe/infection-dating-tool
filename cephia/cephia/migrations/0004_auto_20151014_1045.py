# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0003_auto_20150821_1358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transferinrow',
            old_name='receiving_site',
            new_name='laboratory',
        ),
    ]
