# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    
    def add_spec_type(apps, schema_editor):

        model = apps.get_model("cephia", "SpecimenType")
        model.objects.all().delete()

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


        for st in spec_type_list:
            if "." in st['type']:
                spec_group = st['type'].split(".")[0]
                spec_type = st['type']
            else:
                spec_type = st['type']
                spec_group = st['type']

            model.objects.create(spec_type=spec_type, spec_group=spec_group, name=st['name'])
            
    dependencies = [
        ('cephia', '0031_auto_20150616_2156'),
    ]
    
    operations = [
        migrations.RunPython(add_spec_type),
    ]

