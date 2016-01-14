# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0008_diagnostictesthistory_adjusted_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testpropertyestimate',
            old_name='diagnostic_test',
            new_name='test',
        ),
    ]
