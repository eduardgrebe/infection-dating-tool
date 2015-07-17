# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0055_auto_20150715_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileinfo',
            name='priority',
            field=models.IntegerField(default=1),
        ),
    ]
