# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0056_fileinfo_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specimen',
            name='source_study',
            field=models.ForeignKey(blank=True, to='cephia.Study', null=True),
        ),
    ]
