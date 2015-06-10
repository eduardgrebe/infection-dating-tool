# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0013_auto_20150610_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferinrow',
            name='date_processed',
            field=models.DateTimeField(default='2015-01-01 00:00', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transferinrow',
            name='error_message',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='transferinrow',
            name='fileinfo',
            field=models.ForeignKey(default=1, to='cephia.FileInfo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transferinrow',
            name='state',
            field=models.CharField(default='pending', max_length=10, choices=[(b'pending', b'Pending'), (b'processed', b'Processed'), (b'error', b'Error')]),
            preserve_default=False,
        ),
    ]
