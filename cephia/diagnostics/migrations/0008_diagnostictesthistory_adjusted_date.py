# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0007_auto_20160114_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnostictesthistory',
            name='adjusted_date',
            field=models.DateField(null=True),
        ),
    ]
