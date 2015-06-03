# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0004_fileinfo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fileinfo',
            old_name='file',
            new_name='data_file',
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='message',
            field=models.TextField(null=True, blank=True),
        ),
    ]
