# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_locations(apps, schema_editor):

    model = apps.get_model("cephia", "Location")

    site_list = [{'name':'PHE',
                  'description':'PHE Location'},
                 {'name':'BSRI',
                  'description':'BSRI Location'}]


    for site in site_list:
        model.objects.create(name=site['name'], description=site['description'])
        
class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0004_auto_20151015_1654'),
    ]

    operations = [
        migrations.RunPython(add_locations),
    ]

