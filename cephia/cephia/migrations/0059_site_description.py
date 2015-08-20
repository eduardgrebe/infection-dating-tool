# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations



class Migration(migrations.Migration):
    def add_spec_type(apps, schema_editor):

        model = apps.get_model("cephia", "Site")

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

    dependencies = [
        ('cephia', '0059_auto_20150820_1004'),
    ]

    operations = [
        migrations.RunPython(add_spec_type),
    ]
