# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0012_auto_20150825_1411'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transferinrow',
            old_name='drawdate_day',
            new_name='drawdate_dd',
        ),
        migrations.RenameField(
            model_name='transferinrow',
            old_name='drawdate_month',
            new_name='drawdate_mm',
        ),
        migrations.RenameField(
            model_name='transferinrow',
            old_name='drawdate_year',
            new_name='drawdate_yyyy',
        ),
        migrations.RemoveField(
            model_name='transferinrow',
            name='visit_linkage',
        ),
    ]
