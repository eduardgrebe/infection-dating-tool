# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0010_auto_20150609_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='subject',
            field=models.ForeignKey(default=None, blank=True, to='cephia.Subject', null=True),
        ),
    ]
