# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0013_remove_diagnostictesthistory_ignore'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnostictesthistory',
            name='ignore',
            field=models.BooleanField(default=False),
        ),
    ]
