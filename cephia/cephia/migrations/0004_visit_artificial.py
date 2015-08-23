# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0003_auto_20150823_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='artificial',
            field=models.BooleanField(default=False),
        ),
    ]
