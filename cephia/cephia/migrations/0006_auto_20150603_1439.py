# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0005_auto_20150603_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileinfo',
            name='message',
            field=models.TextField(default='test', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='state',
            field=models.CharField(default=b'PE', max_length=2, choices=[(b'PE', b'PENDING'), (b'IM', b'IMPORTED'), (b'ER', b'ERROR')]),
        ),
    ]
