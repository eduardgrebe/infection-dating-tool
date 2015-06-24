# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    def add_spec_type(apps, schema_editor):

        model = apps.get_model("cephia", "SpecimenType")

        spec_type_list= [{'type':'1', 'name':'Whole Blood'},
            {'type':'2', 'name':'DBS'},
            {'type':'3', 'name':'Serum'},
            {'type':'4.1', 'name':'Urine / Nothing'},
            {'type':'4.2', 'name':'Urine / Azide'},
            {'type':'5.1', 'name':'Stool / Nothing'},
            {'type':'5.2', 'name':'Stool / RNAlater'},
            {'type':'6', 'name':'Saliva'},
            {'type':'7', 'name':'PBMC'},
            {'type':'8', 'name':'Plasma'},
            {'type':'9', 'name':'Hair'},
            {'type':'10.1', 'name':'Buccal swab / Nothing'},
            {'type':'10.2', 'name':'Buccal swab / Buffer'}]


        for spec_type in spec_type_list:
            if "." in spec_type['type']:
                spec = spec_type['type'].split(".")[0]
                spec_group = spec_type['type'].split(".")[1]
            else:
                spec = spec_type['type']
                spec_group = 0

            model.objects.create(spec_type=spec, spec_group=spec_group, name=spec_type['name'])

    dependencies = [
        ('cephia', '0018_auto_20150610_1414'),
    ]

    operations = [
        migrations.RunPython(add_spec_type),
    ]
