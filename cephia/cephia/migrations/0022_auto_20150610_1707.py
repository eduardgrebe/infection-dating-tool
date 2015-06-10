# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0021_specimen_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specimen',
            name='transfer_in_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
