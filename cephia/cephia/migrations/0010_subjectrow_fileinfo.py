# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0009_auto_20150604_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectrow',
            name='fileinfo',
            field=models.ForeignKey(default=18, to='cephia.FileInfo'),
            preserve_default=False,
        ),
    ]
