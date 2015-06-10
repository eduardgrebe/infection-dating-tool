# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0008_auto_20150608_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='visit_label',
            field=models.CharField(default='xxx', max_length=255),
            preserve_default=False,
        ),
    ]
