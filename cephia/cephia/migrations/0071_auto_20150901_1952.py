# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0070_auto_20150901_1050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transferoutrow',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='transferoutrow',
            name='fileinfo',
        ),
        migrations.DeleteModel(
            name='TransferOutRow',
        ),
    ]
