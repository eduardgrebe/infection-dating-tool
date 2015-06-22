# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0049_auto_20150622_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='specimen',
            name='site',
            field=models.ForeignKey(blank=True, to='cephia.Site', null=True),
        ),
    ]
