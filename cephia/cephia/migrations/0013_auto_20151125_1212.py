# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0012_auto_20151125_1155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='panel',
            name='specimen_type',
        ),
        migrations.RemoveField(
            model_name='panelmemberships',
            name='panel',
        ),
        migrations.RemoveField(
            model_name='panelmemberships',
            name='visit',
        ),
        migrations.DeleteModel(
            name='Panel',
        ),
        migrations.DeleteModel(
            name='PanelMemberships',
        ),
    ]
