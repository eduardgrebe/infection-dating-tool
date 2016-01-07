# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0019_auto_20160103_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panels',
            name='description',
            field=models.TextField(),
        ),
    ]
