# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_study(apps, schema_editor):

    model = apps.get_model("cephia", "Study")

    source_study_list = [{'name':'OPTIONS',
                          'description':'Options study'}]


    for study in source_study_list:
        model.objects.create(name=study['name'], description=study['description'])

class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0078_transferinrow_roll_up'),
    ]

    operations = [
        migrations.RunPython(add_study),
    ]

