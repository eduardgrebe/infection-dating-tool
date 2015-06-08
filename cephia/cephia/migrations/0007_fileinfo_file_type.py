# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0006_source_visit_visitrow'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileinfo',
            name='file_type',
            field=models.CharField(default='subject', max_length=20, choices=[(b'subject', b'Subject'), (b'visit', b'Visit')]),
            preserve_default=False,
        ),
    ]
