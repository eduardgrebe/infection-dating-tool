# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_countries(apps, schema_editor):

    model = apps.get_model("cephia", "Region")
    regionx = model.objects.create(name='RegionX')
    
    model = apps.get_model("cephia", "Country")
    model.objects.create(name='South Africa', code="za", region=regionx)

class Migration(migrations.Migration):
    
    dependencies = [
        ('cephia', '0002_auto_20150601_0925'),
    ]

    operations = [
        migrations.RunPython(add_countries),
    ]
