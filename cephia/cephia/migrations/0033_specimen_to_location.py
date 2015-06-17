# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0032_auto_20150616_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='specimen',
            name='to_location',
            field=models.ForeignKey(blank=True, to='cephia.Location', null=True),
        ),
    ]
