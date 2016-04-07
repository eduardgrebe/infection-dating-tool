# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0012_auto_20160201_1307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diagnostictesthistory',
            name='ignore',
        ),
    ]
