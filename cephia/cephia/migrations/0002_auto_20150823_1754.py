# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='missingtransferoutrow',
            name='fileinfo',
        ),
        migrations.RenameField(
            model_name='visit',
            old_name='visit_cd4',
            new_name='cd4_count',
        ),
        migrations.RenameField(
            model_name='visit',
            old_name='visit_hepatitis',
            new_name='hepatitis',
        ),
        migrations.RenameField(
            model_name='visit',
            old_name='visit_pregnant',
            new_name='pregnant',
        ),
        migrations.RenameField(
            model_name='visit',
            old_name='scope_visit_ec',
            new_name='scopevisit_ec',
        ),
        migrations.RenameField(
            model_name='visit',
            old_name='patient_label',
            new_name='subject_label',
        ),
        migrations.RenameField(
            model_name='visit',
            old_name='visit_vl',
            new_name='vl',
        ),
        migrations.DeleteModel(
            name='MissingTransferOutRow',
        ),
    ]
