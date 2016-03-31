# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import lib.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0032_auto_20160315_1552'),
        ('assay', '0004_auto_20160329_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssayRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('run_date', models.DateField()),
                ('comment', models.CharField(max_length=255, null=True)),
                ('assay', lib.fields.ProtectedForeignKey(to='cephia.Assay', on_delete=django.db.models.deletion.PROTECT)),
                ('fileinfo', lib.fields.ProtectedForeignKey(to='cephia.FileInfo', on_delete=django.db.models.deletion.PROTECT)),
                ('laboratory', lib.fields.ProtectedForeignKey(to='cephia.Laboratory', on_delete=django.db.models.deletion.PROTECT)),
                ('panel', lib.fields.ProtectedForeignKey(to='cephia.Panel', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'db_table': 'cephia_assay_runs',
            },
        ),
        migrations.RemoveField(
            model_name='architectavidityresult',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='architectavidityresult',
            name='panel',
        ),
        migrations.RemoveField(
            model_name='architectunmodifiedresult',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='architectunmodifiedresult',
            name='panel',
        ),
        migrations.RemoveField(
            model_name='bedresult',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='bedresult',
            name='panel',
        ),
        migrations.RemoveField(
            model_name='bioradaviditycdcresult',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='bioradaviditycdcresult',
            name='panel',
        ),
        migrations.RemoveField(
            model_name='bioradavidityglasgowresult',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='bioradavidityglasgowresult',
            name='panel',
        ),
        migrations.RemoveField(
            model_name='bioradavidityjhuresult',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='bioradavidityjhuresult',
            name='panel',
        ),
        migrations.RemoveField(
            model_name='geeniusresult',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='geeniusresult',
            name='panel',
        ),
        migrations.RemoveField(
            model_name='idev3result',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='idev3result',
            name='panel',
        ),
        migrations.RemoveField(
            model_name='lagmaximresult',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='lagmaximresult',
            name='panel',
        ),
        migrations.RemoveField(
            model_name='lagsediaresult',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='lagsediaresult',
            name='panel',
        ),
        migrations.RemoveField(
            model_name='lsvitrosdiluentresult',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='lsvitrosdiluentresult',
            name='panel',
        ),
        migrations.RemoveField(
            model_name='lsvitrosplasmaresult',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='lsvitrosplasmaresult',
            name='panel',
        ),
        migrations.RemoveField(
            model_name='luminexcdcresult',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='luminexcdcresult',
            name='panel',
        ),
        migrations.RemoveField(
            model_name='vitrosavidityresult',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='vitrosavidityresult',
            name='panel',
        ),
        migrations.AddField(
            model_name='architectavidityresult',
            name='assay_run',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assay.AssayRun', null=True),
        ),
        migrations.AddField(
            model_name='architectunmodifiedresult',
            name='assay_run',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assay.AssayRun', null=True),
        ),
        migrations.AddField(
            model_name='assayresult',
            name='assay_run',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assay.AssayRun', null=True),
        ),
        migrations.AddField(
            model_name='bedresult',
            name='assay_run',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assay.AssayRun', null=True),
        ),
        migrations.AddField(
            model_name='bioradaviditycdcresult',
            name='assay_run',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assay.AssayRun', null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityglasgowresult',
            name='assay_run',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assay.AssayRun', null=True),
        ),
        migrations.AddField(
            model_name='bioradavidityjhuresult',
            name='assay_run',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assay.AssayRun', null=True),
        ),
        migrations.AddField(
            model_name='geeniusresult',
            name='assay_run',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assay.AssayRun', null=True),
        ),
        migrations.AddField(
            model_name='idev3result',
            name='assay_run',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assay.AssayRun', null=True),
        ),
        migrations.AddField(
            model_name='lagmaximresult',
            name='assay_run',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assay.AssayRun', null=True),
        ),
        migrations.AddField(
            model_name='lagsediaresult',
            name='assay_run',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assay.AssayRun', null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosdiluentresult',
            name='assay_run',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assay.AssayRun', null=True),
        ),
        migrations.AddField(
            model_name='lsvitrosplasmaresult',
            name='assay_run',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assay.AssayRun', null=True),
        ),
        migrations.AddField(
            model_name='luminexcdcresult',
            name='assay_run',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assay.AssayRun', null=True),
        ),
        migrations.AddField(
            model_name='vitrosavidityresult',
            name='assay_run',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assay.AssayRun', null=True),
        ),
    ]
