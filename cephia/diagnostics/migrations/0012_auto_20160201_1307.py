# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0011_diagnostictesthistory_ignore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostictesthistory',
            name='ignore',
            field=models.BooleanField(default=False),
        ),
    ]
