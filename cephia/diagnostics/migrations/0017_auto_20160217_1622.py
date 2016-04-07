# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import cephia.fields


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0016_auto_20160211_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostictesthistoryrow',
            name='fileinfo',
            field=cephia.fields.ProtectedForeignKey(to='cephia.FileInfo', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
