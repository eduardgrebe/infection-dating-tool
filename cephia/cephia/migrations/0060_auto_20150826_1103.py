# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0059_site_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aliquotrow',
            name='fileinfo',
        ),
        migrations.DeleteModel(
            name='AliquotRow',
        ),
    ]
