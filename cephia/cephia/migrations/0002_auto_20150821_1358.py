# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_spec_types(apps, schema_editor):
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
                     {'type':'10.2', 'name':'Buccal swab / Buffer'}
                 ]

    for st in spec_type_list:
        if "." in st['type']:
            spec_group = st['type'].split(".")[0]
            spec_type = st['type']
        else:
            spec_type = st['type']
            spec_group = st['type']

        model.objects.create(spec_type=spec_type, spec_group=spec_group, name=st['name'])

def add_studies(apps, schema_editor):

    model = apps.get_model("cephia", "Study")

    source_study_list = [{'name':'IAVI',
                          'description':'IAVI study - from core lab in London'},
                         {'name':'UCSD',
                          'description':'UCSD study, San Diego, CA'},
                         {'name':'SCOPE',
                          'description':'SCOPE study, San Francisco, CA'},
                         {'name':'AMPLIAR',
                          'description':'AMPLIAR study, Brazil'},
                         {'name':'SFMHS',
                          'description':'San Francisco Men’s Health Study'},
                         {'name':'CTS',
                          'description':'Blood bank - Blood Systems Testing Lab (Description to be updated)'},
                         {'name':'BRAZIL',
                          'description':'Blood bank - Brazil'},
                         {'name':'SANBS',
                          'description':'Blood bank - SANBS'},
                         {'name':'CAPRISA',
                          'description':'CAPRISA study - South Africa'},
                         {'name':'FPSHSP',
                          'description':'Fundação Pro-Sangue-Hemocentro de São Paulo, Brazil'},
                         {'name':'GAMA',
                          'description':'CRESIB malaria cohort'},
                         {'name':'IMPACTA',
                          'description':'Asociación Civil Impacta Saludy Educación'},
                         {'name':'ARC',
                          'description':'Blood bank - American Red Cross'},
                         {'name':'OPTIONS',
                          'description':'Options study'}]


    for study in source_study_list:
        model.objects.create(name=study['name'], description=study['description'])

def add_ethnicities(apps, schema_editor):

    model = apps.get_model("cephia", "Ethnicity")

    ethnicities = ['Hispanic/Latino',
                   'Black African',
                   'Brazilian',
                   'Multiethnic',
                   'African American',
                   'White',
                   'Other',
                   'Unknown',
                   'Asian']

    for ethnicity in ethnicities:
        model.objects.create(name=ethnicity)

def add_labs(apps, schema_editor):
    model = apps.get_model("cephia", "Laboratory")
    
    source_site_list = [{'name':'HPA',
                         'description':'Health Protection Agency'},
                        {'name':'BSRI',
                         'description':'Blood Systems Research Institue'},
                        {'name':'CDCD',
                         'description':'Centers for Disease Control and Prevention, Domestic'},
                        {'name':'CDCI',
                         'description':'Centers for Disease Control and Prevention, International'},
                        {'name':'JHU',
                         'description':'Johns Hopkins University'},
                        {'name':'ISI',
                         'description':'Instituto Superiore di Sanita, Rome Italy'},
                        {'name':'Maxim',
                         'description':'Maxim Biomedical Inc, Rockville, Maryland'},
                        {'name':'BioRad',
                         'description':'BioRad, Hercules, CA'},
                        {'name':'Calypte',
                         'description':'Calypte Biomedical, Portland, OR)'},
                        {'name':'CBIO',
                         'description':'ChemBio, Brazil'},
                        {'name':'FDA',
                         'description':'Food and Drug Administration; Usha Sharma'},
                        {'name':'Immunetics',
                         'description':'Immunetics; Andrew Levin, Boston'},
                        {'name':'KEM',
                         'description':'Kliniken Essen-Mitte, Germany'},
                        {'name':'Metabolistics',
                         'description':'Metabolistics, Canada'},
                        {'name':'Pitt',
                         'description':'Universityof Pittsburgh'},
                        {'name':'Roederer',
                         'description':'Mario Roederer, National Institues of Health'},
                        {'name':'Sedia',
                         'description':'Sedia Biosciences, Portland, OR'},
                        {'name':'USC',
                         'description':'University of Southern California, Ha Youn Lee'},
                        {'name':'BGI',
                         'description':'Beijing Genomics Institue, Hong Kong'},
                        {'name':'CEK',
                         'description':'CEK (Centro Esther Koplowitz), Barcelona, Spain'},
                        {'name':'Duke',
                         'description':'Duke University, Georgia Tomaras lab'},
                        {'name':'ADi',
                         'description':'Antigen Discovery, Irvine'},
                        {'name':'AbDiag',
                         'description':'RPC Diagnostic Systems, Russia'},
                        {'name':'Avioq',
                         'description':'Avioq, Inc., North Carolina'},
                        {'name':'UCD',
                         'description':'University College Dublin'},
                        {'name':'UCSF-McCune',
                         'description':'Ivan Vujikovic-Cvijin, McCune Laboratory'},
                        {'name':'Maldarelli',
                         'description':'Frank Malderelli, National Institues of Health'},]

    model.objects.all().delete()
        
    for site in source_site_list:
        model.objects.create(name=site['name'], description=site['description'])


class Migration(migrations.Migration):
            
    dependencies = [
        ('cephia', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_spec_types),
        migrations.RunPython(add_studies),
        migrations.RunPython(add_ethnicities),
        migrations.RunPython(add_labs),
    ]
