# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0020_auto_20150610_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='specimen',
            name='subject',
            field=models.ForeignKey(blank=True, to='cephia.Subject', null=True),
        ),
    ]
