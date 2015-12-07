# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_studies(apps, schema_editor):

    model = apps.get_model("cephia", "Study")

    source_study_list = [{'name':'SERACARE',
                          'description':''}]


    for study in source_study_list:
        model.objects.create(name=study['name'], description=study['description'])

class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0012_auto_20151204_1246'),
    ]

    operations = [
        migrations.RunPython(add_studies),
    ]
