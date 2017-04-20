# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import cephia.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0027_historicalaliquotrow_historicalsubjectrow_historicaltransferinrow_historicaltransferoutrow_historica'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliquotrow',
            name='comment',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AlterField(
            model_name='aliquotrow',
            name='fileinfo',
            field=cephia.fields.ProtectedForeignKey(to='cephia.FileInfo', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='aliquotrow',
            name='specimen',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='region',
            field=cephia.fields.ProtectedForeignKey(to='cephia.Region', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='historicalaliquotrow',
            name='comment',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AlterField(
            model_name='historicalaliquotrow',
            name='fileinfo',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.FileInfo', null=True),
        ),
        migrations.AlterField(
            model_name='historicalaliquotrow',
            name='specimen',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='historicalspecimen',
            name='location',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Location', null=True),
        ),
        migrations.AlterField(
            model_name='historicalspecimen',
            name='parent',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='historicalspecimen',
            name='shipped_to',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Laboratory', null=True),
        ),
        migrations.AlterField(
            model_name='historicalspecimen',
            name='source_study',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Study', null=True),
        ),
        migrations.AlterField(
            model_name='historicalspecimen',
            name='specimen_type',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.SpecimenType', null=True),
        ),
        migrations.AlterField(
            model_name='historicalspecimen',
            name='subject',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Subject', null=True),
        ),
        migrations.AlterField(
            model_name='historicalspecimen',
            name='visit',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Visit', null=True),
        ),
        migrations.AlterField(
            model_name='historicalsubject',
            name='country',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Country', null=True),
        ),
        migrations.AlterField(
            model_name='historicalsubject',
            name='population_group',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Ethnicity', null=True),
        ),
        migrations.AlterField(
            model_name='historicalsubject',
            name='source_study',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Study', null=True),
        ),
        migrations.AlterField(
            model_name='historicalsubject',
            name='subject_eddi',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.SubjectEDDI', null=True),
        ),
        migrations.AlterField(
            model_name='historicalsubject',
            name='subject_eddi_status',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.SubjectEDDIStatus', null=True),
        ),
        migrations.AlterField(
            model_name='historicalsubject',
            name='subtype',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Subtype', null=True),
        ),
        migrations.AlterField(
            model_name='historicalsubjectrow',
            name='comment',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AlterField(
            model_name='historicalsubjectrow',
            name='fileinfo',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.FileInfo', null=True),
        ),
        migrations.AlterField(
            model_name='historicalsubjectrow',
            name='subject',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Subject', null=True),
        ),
        migrations.AlterField(
            model_name='historicaltransferinrow',
            name='comment',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AlterField(
            model_name='historicaltransferinrow',
            name='fileinfo',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.FileInfo', null=True),
        ),
        migrations.AlterField(
            model_name='historicaltransferinrow',
            name='specimen',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='historicaltransferoutrow',
            name='comment',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AlterField(
            model_name='historicaltransferoutrow',
            name='fileinfo',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.FileInfo', null=True),
        ),
        migrations.AlterField(
            model_name='historicaltransferoutrow',
            name='specimen',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='historicalvisit',
            name='source_study',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Study', null=True),
        ),
        migrations.AlterField(
            model_name='historicalvisit',
            name='subject',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Subject', null=True),
        ),
        migrations.AlterField(
            model_name='historicalvisit',
            name='visit_eddi',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.VisitEDDI', null=True),
        ),
        migrations.AlterField(
            model_name='historicalvisitrow',
            name='comment',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AlterField(
            model_name='historicalvisitrow',
            name='fileinfo',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.FileInfo', null=True),
        ),
        migrations.AlterField(
            model_name='historicalvisitrow',
            name='visit',
            field=cephia.fields.ProtectedForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, db_constraint=False, blank=True, to='cephia.Visit', null=True),
        ),
        migrations.AlterField(
            model_name='panel',
            name='specimen_type',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cephia.SpecimenType', null=True),
        ),
        migrations.AlterField(
            model_name='panelmemberships',
            name='panel',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cephia.Panel', null=True),
        ),
        migrations.AlterField(
            model_name='panelmemberships',
            name='visit',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cephia.Visit', null=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='location',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='cephia.Location', null=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='parent',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='shipped_to',
            field=cephia.fields.ProtectedForeignKey(related_name='shipped_to', on_delete=django.db.models.deletion.PROTECT, blank=True, to='cephia.Laboratory', null=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='source_study',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='cephia.Study', null=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='specimen_type',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='cephia.SpecimenType', null=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='subject',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cephia.Subject', null=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='visit',
            field=cephia.fields.ProtectedForeignKey(related_name='visit', on_delete=django.db.models.deletion.PROTECT, to='cephia.Visit', null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='country',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='cephia.Country', null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='population_group',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='cephia.Ethnicity', null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='source_study',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='cephia.Study', null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='subject_eddi',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='cephia.SubjectEDDI', null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='subject_eddi_status',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='cephia.SubjectEDDIStatus', null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='subtype',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='cephia.Subtype', null=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='comment',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='fileinfo',
            field=cephia.fields.ProtectedForeignKey(to='cephia.FileInfo', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='subject',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cephia.Subject', null=True),
        ),
        migrations.AlterField(
            model_name='transferinrow',
            name='comment',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AlterField(
            model_name='transferinrow',
            name='fileinfo',
            field=cephia.fields.ProtectedForeignKey(to='cephia.FileInfo', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='transferinrow',
            name='specimen',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='transferoutrow',
            name='comment',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AlterField(
            model_name='transferoutrow',
            name='fileinfo',
            field=cephia.fields.ProtectedForeignKey(to='cephia.FileInfo', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='transferoutrow',
            name='specimen',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cephia.Specimen', null=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='source_study',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='cephia.Study', null=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='subject',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, blank=True, to='cephia.Subject', null=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='visit_eddi',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='cephia.VisitEDDI', null=True),
        ),
        migrations.AlterField(
            model_name='visitrow',
            name='comment',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AlterField(
            model_name='visitrow',
            name='fileinfo',
            field=cephia.fields.ProtectedForeignKey(to='cephia.FileInfo', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='visitrow',
            name='visit',
            field=cephia.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cephia.Visit', null=True),
        ),
    ]
