# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0023_auto_20160429_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vitrosavidityresult',
            name='AI_recalc',
        ),
        migrations.RemoveField(
            model_name='vitrosavidityresult',
            name='treated_SCO',
        ),
        migrations.RemoveField(
            model_name='vitrosavidityresult',
            name='untreated_SCO',
        ),
        migrations.RemoveField(
            model_name='vitrosavidityresultrow',
            name='AI_recalc',
        ),
        migrations.RemoveField(
            model_name='vitrosavidityresultrow',
            name='treated_SCO',
        ),
        migrations.RemoveField(
            model_name='vitrosavidityresultrow',
            name='untreated_SCO',
        ),
        migrations.AddField(
            model_name='vitrosavidityresult',
            name='AI_reported',
            field=models.FloatField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresult',
            name='treated_guanidine_OD',
            field=models.FloatField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresult',
            name='untreated_pbs_OD',
            field=models.FloatField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresult',
            name='well_treated_guanidine',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresult',
            name='well_untreated_pbs',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresultrow',
            name='AI_reported',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresultrow',
            name='treated_guanidine_OD',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresultrow',
            name='untreated_pbs_OD',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresultrow',
            name='well_treated_guanidine',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresultrow',
            name='well_untreated_pbs',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='vitrosavidityresult',
            name='AI',
            field=models.FloatField(max_length=255, null=True),
        ),
    ]
