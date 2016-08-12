import logging
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from models import (Country, FileInfo, SubjectRow, Subject, Ethnicity, Visit,
                    VisitRow, Laboratory, Specimen, SpecimenType, TransferInRow,
                    Study, TransferOutRow, AliquotRow)
from diagnostics.models import DiagnosticTestHistoryRow
from forms import (FileInfoForm, RowCommentForm, SubjectFilterForm,
                   VisitFilterForm, RowFilterForm, SpecimenFilterForm,
                   FileInfoFilterForm, VisitExportForm)
from django.forms.models import model_to_dict
from csv_helper import get_csv_response
from datetime import datetime
import json
from collections import OrderedDict
from django.utils import timezone
import os
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test

logger = logging.getLogger(__name__)

@login_required
def home(request, file_id=None, template="cephia/home.html"):
    if request.method == "GET":
        context = {}
        subject_file = FileInfo.objects.filter(file_type='subject').order_by('-created').first()
        visit_file = FileInfo.objects.filter(file_type='visit').order_by('-created').first()
        transfer_in_file = FileInfo.objects.filter(file_type='transfer_in').order_by('-created').first()
        aliquot_file = FileInfo.objects.filter(file_type='aliquot').order_by('-created').first()
        transfer_out_file = FileInfo.objects.filter(file_type='transfer_out').order_by('-created').first()
        
        subject_rows = SubjectRow.objects.filter(fileinfo=subject_file)
        visit_rows = VisitRow.objects.filter(fileinfo=visit_file)
        transfer_in_rows = TransferInRow.objects.filter(fileinfo=transfer_in_file)
        aliquot_rows = AliquotRow.objects.filter(fileinfo=aliquot_file)
        transfer_out_rows = TransferOutRow.objects.filter(fileinfo=transfer_out_file)

        form = FileInfoForm()
        form.filter_options(request)
        
        context['form'] = form
        context['subject_file'] = subject_file
        context['visit_file'] = visit_file
        context['transfer_in_file'] = transfer_in_file
        context['transfer_out_file'] = transfer_out_file
        context['aliquot_file'] = aliquot_file

        context['subject_errors'] = subject_rows.filter(state='error').count()
        context['visit_errors'] = visit_rows.filter(state='error').count()
        context['aliquot_errors'] = aliquot_rows.filter(state='error').count()
        context['transfer_in_errors'] = transfer_in_rows.filter(state='error').count()
        context['transfer_out_errors'] = transfer_out_rows.filter(state='error').count()

        context['subject_validated'] = subject_rows.filter(state='validated').count()
        context['visit_validated'] = visit_rows.filter(state='validated').count()
        context['aliquot_validated'] = aliquot_rows.filter(state='validated').count()
        context['transfer_in_validated'] = transfer_in_rows.filter(state='validated').count()
        context['transfer_out_validated'] = transfer_out_rows.filter(state='validated').count()
        
        context['subject_processed'] = subject_rows.filter(state='processed').count()
        context['visit_processed'] = visit_rows.filter(state='processed').count()
        context['aliquot_processed'] = aliquot_rows.filter(state='processed').count()
        context['transfer_in_processed'] = transfer_in_rows.filter(state='processed').count()
        context['transfer_out_processed'] = transfer_out_rows.filter(state='processed').count()

        context['subject_total'] = subject_rows.count()
        context['visit_total'] = visit_rows.count()
        context['aliquot_total'] = aliquot_rows.count()
        context['transfer_in_total'] = transfer_in_rows.count()
        context['transfer_out_total'] = transfer_out_rows.count()

    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def table_management(request, template="cephia/tms_home.html"):
    context = {}
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def countries(request, template="cephia/countries.html"):
    context = {}
    countries = Country.objects.all().order_by("name")
    context['countries'] = countries
    
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.is_staff)
def ethnicities(request, template="cephia/ethnicities.html"):
    context = {}
    ethnicities = Ethnicity.objects.all()
    context['ethnicities'] = ethnicities
    
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def studies(request, template="cephia/studies.html"):
    context = {}
    studies = Study.objects.all()
    context['studies'] = studies
    
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def labs(request, template="cephia/sites.html"):
    context = {}
    sites = Laboratory.objects.all()
    context['sites'] = sites
    
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def subjects(request, template="cephia/subjects.html"):
    context = {}
    subjects = Subject.objects.all()

    form = SubjectFilterForm(request.GET or None)
    if form.is_valid():
        subjects = form.filter(subjects)

    context['subjects'] = subjects
    context['form'] = form

    if 'csv' in request.GET:
        try:
            response, writer = get_csv_response('subjects_%s.csv' % datetime.today().strftime('%d%b%Y_%H%M'))
            headers = model_to_dict(subjects[0]).keys()

            writer.writerow(headers)

            for subject in subjects:
                d = model_to_dict(subject)
                content = [ d[x] for x in headers ]
                writer.writerow(content)

            return response
        except Exception, e:
            logger.exception(e)
            messages.error(request, 'Failed to download file')
    else:
        return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def visit_export(request, template='cephia/visit_export.html'):
    context = {}
    export_form = VisitExportForm(request.POST or None, request.FILES or None)
    context['export_form'] = export_form

    if request.method == 'POST' and export_form.is_valid():
        visits = export_form.get_visits()
        filename = 'visits_%s.csv' % datetime.today().strftime('%d%b%Y_%H%M')
        response, writer = get_csv_response(filename)
        writer.writerow(['visit_id'])
        for visit in visits:
            writer.writerow([visit.pk])
        return response
    
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def visits(request, visit_id=None, template="cephia/visits.html"):
    context = {}
    visits = Visit.objects.all()
    if visit_id is not None:
        visits = visits.filter(pk=visit_id)

    form = VisitFilterForm(request.GET or None)
    if form.is_valid():
        visits = form.filter(visits)

    context['visits'] = visits
    context['form'] = form

    if 'csv' in request.GET:
        try:
            response, writer = get_csv_response('visits_%s.csv' % datetime.today().strftime('%d%b%Y_%H%M'))
            headers = model_to_dict(visits[0]).keys()

            writer.writerow(headers)

            for visit in visits:
                d = model_to_dict(visit)
                content = [ d[x] for x in headers ]
                writer.writerow(content)

            return response
        except Exception, e:
            logger.exception(e)
            messages.error(request, 'Failed to download file')
    else:
        return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def specimen(request, template="cephia/specimen.html"):
    context = {}
    form = SpecimenFilterForm(request.GET or None)

    if form.is_valid():
        specimen = form.filter()
    else:
        specimen = Specimen.objects.all().order_by('specimen_label', 'parent_label')

    context['specimen'] = specimen
    context['form'] = form

    if 'csv' in request.GET:
        try:
            response, writer = get_csv_response('specimen_%s.csv' % datetime.today().strftime('%d%b%Y_%H%M'))
            headers = model_to_dict(specimen[0]).keys()

            writer.writerow(headers)

            for spec in specimen:
                d = model_to_dict(spec)
                content = [ d[x] for x in headers ]
                writer.writerow(content)

            return response
        except Exception, e:
            logger.exception(e)
            messages.error(request, 'Failed to download file')
    else:
        return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def specimen_type(request, template="cephia/specimen_type.html"):
    context = {}
    spec_type = SpecimenType.objects.all()
    context['spec_type'] = spec_type
    
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.is_staff)
def file_info(request, template="cephia/file_info.html"):
    context = {}

    if request.method == "GET":
        upload_form = FileInfoForm()
        upload_form.filter_options(request)
        filter_form = FileInfoFilterForm(request.GET or None)
        if filter_form.is_valid():
            files = filter_form.filter()
        else:
            files = FileInfo.objects.all().order_by('-created')

        context['files'] = files
        context['files_in_process'] = list(FileInfo.objects.filter(task_id__isnull=False).order_by('-created'))
        context['upload_form'] = upload_form
        context['filter_form'] = filter_form
        
    return render_to_response(template, context, context_instance=RequestContext(request))

   
@login_required
@user_passes_test(lambda u: u.is_staff)
def row_info(request, file_id, template=None):
    if request.method == 'GET':
        context = {}
        fileinfo = FileInfo.objects.get(pk=file_id)
        comment_form = RowCommentForm()
        
        filter_form = RowFilterForm(request.GET or None)
        if filter_form.is_valid():
            rows, template = filter_form.filter(fileinfo)
        else:
            rows, template = filter_form.filter(fileinfo)

        
        context['rows'] = rows
        context['file_id'] = fileinfo.id
        context['file'] = fileinfo.filename()
        context['has_errors'] = rows.filter(state='error').exists()
        context['filter_form'] = filter_form
        context['comment_form'] = comment_form
        return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def download_file(request, file_id):
    try:
        if request.method == "GET":
            download_file = FileInfo.objects.get(pk=file_id)
            response = HttpResponse(download_file.data_file, content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="%s"' % (download_file.filename())
            return response
    except Exception, e:
        logger.exception(e)
        messages.error(request, 'Failed to download file')
        return HttpResponseRedirect(reverse('file_info'))


@login_required
@user_passes_test(lambda u: u.is_staff)
def upload_file(request):
    try:
        FILE_PRIORITIES = {
            'diagnostic_test': 0,
            'protocol_lookup': 0,
            'test_history': 0,
            'test_property': 0,
            'subject': 1,
            'visit': 2,
            'transfer_in': 3,
            'aliquot': 4,
            'transfer_out': 5,
        }

        if request.method == "POST":
            post_data = request.POST.copy()
            if post_data.get("priority"):
                priority = post_data.get("priority")
                file_type = [k for k , v in FILE_PRIORITIES.iteritems() if u"%s" % v == priority][0]
                post_data.__setitem__('file_type', file_type)
            else:
                priority = FILE_PRIORITIES[request.POST.get('file_type')]
                post_data.__setitem__('priority', priority)
    
            form = FileInfoForm(post_data, request.FILES)
            form.filter_options(request)
            form.fields['laboratory'].required = False
            form.fields['specimen_label_type'].required = False
            if form.is_valid():
                new_file = form.save()
                if new_file.file_type == 'test_history':
                    new_file.get_handler().parse()
                    new_file.get_handler().validate()
                    new_file.get_handler().process()
                elif new_file.file_type in ['diagnostic_test','protocol_lookup', 'test_property']:
                    new_file.get_handler().process()
                messages.add_message(request, messages.SUCCESS, 'Successfully uploaded file')
            else:
                messages.add_message(request, messages.ERROR, 'Failed to upload file: %s' % dict(form._errors))
    
            return HttpResponseRedirect(reverse('file_info'))

    except Exception, e:
        logger.exception(e)
        messages.add_message(request, messages.ERROR, 'Failed to upload file')
        return HttpResponseRedirect(reverse('file_info'))


@login_required
@user_passes_test(lambda u: u.is_staff)
def parse_file(request, file_id):
    try:
        file_to_parse = FileInfo.objects.get(pk=file_id)
        file_handler = file_to_parse.get_handler()
        msg = file_handler.validate_file()

        if msg:
            messages.add_message(request, messages.WARNING, msg)

        num_success, num_fail = file_handler.parse()

        fail_msg = 'Failed to import ' + str(num_fail) + ' rows.'
        msg = 'Successfully imported ' + str(num_success) + ' rows.'

        if num_fail > 0:
            file_to_parse.state = 'file_error'
            #messages.add_message(request, messages.ERROR, 'Failed to import ' + str(num_fail) + ' rows. ')
        else:
            file_to_parse.state = 'imported'
            #messages.add_message(request, messages.SUCCESS, 'Successfully imported ' + str(num_success) + ' rows. ')

        file_to_parse.message += fail_msg + '\n' + msg + '\n'
        file_to_parse.save()
    
        return HttpResponseRedirect(reverse('file_info'))
    except Exception, e:
        logger.exception(e)
        messages.add_message(request, messages.ERROR, 'Import failed: ' + e.message)
        file_to_parse.state = 'file_error'
        file_to_parse.message = e.message
        file_to_parse.save()
        return HttpResponseRedirect(reverse('file_info'))

@login_required
@user_passes_test(lambda u: u.is_staff)
def validate_rows(request, file_id):
    try:
        file_to_validate = FileInfo.objects.get(pk=file_id)
        file_handler = file_to_validate.get_handler()

        num_success, num_fail = file_handler.validate()

        fail_msg = 'Failed to validate ' + str(num_fail) + ' rows.'
        msg = 'Successfully validated ' + str(num_success) + ' rows.'

        if num_fail > 0:
            file_to_validate.state = 'row_error'
        else:
            file_to_validate.state = 'validated'

        file_to_validate.message += fail_msg + '\n' + msg + '\n'
        file_to_validate.save()
        
        return HttpResponseRedirect(reverse('file_info'))
    except Exception, e:
        logger.exception(e)
        messages.add_message(request, messages.ERROR, 'Validate failed: ' + e.message)
        file_to_validate.state = 'file_error'
        file_to_validate.message = e.message
        file_to_validate.save()
        return HttpResponseRedirect(reverse('file_info'))


@login_required
@user_passes_test(lambda u: u.is_staff)
def process_file(request, file_id):
    try:
        file_to_process = FileInfo.objects.get(pk=file_id)
        file_handler = file_to_process.get_handler()
        
        num_success, num_fail = file_handler.process()

        fail_msg = 'Failed to process ' + str(num_fail) + ' rows.'
        msg = 'Successfully processed ' + str(num_success) + ' rows.'

        if num_fail > 0:
            messages.add_message(request, messages.WARNING, fail_msg)
            file_to_process.state = 'error'
        else:
            file_to_process.state = 'processed'
    
        messages.add_message(request, messages.SUCCESS, msg)

        file_to_process.message += fail_msg + '\n' + msg + '\n'
        file_to_process.save()

        return HttpResponseRedirect(reverse('file_info'))
    except Exception, e:
        logger.exception(e)
        messages.add_message(request, messages.ERROR, 'Failed to process: ' + e.message)
        file_to_process.state = 'file_error'
        file_to_process.message = e.message
        file_to_process.save()
        return HttpResponseRedirect(reverse('file_info'))


@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_file(request, file_id):
    try:
        file_info = FileInfo.objects.get(pk=file_id)
        file_info.delete()

        messages.add_message(request, messages.SUCCESS, 'File successfully deleted')

        return HttpResponseRedirect(reverse('file_info'))
    except Exception, e:
        logger.exception(e)
        messages.add_message(request, messages.ERROR, 'Could not delete file')
        return HttpResponseRedirect(reverse('file_info'))


@login_required
def export_as_csv(request, file_id):
    try:
        fileinfo = FileInfo.objects.get(pk=file_id)
        state = 'error'

        if fileinfo.file_type == 'subject':
            rows = SubjectRow.objects.filter(fileinfo=fileinfo, state=state)
        elif fileinfo.file_type == 'visit':
            rows = VisitRow.objects.filter(fileinfo=fileinfo, state=state)
        elif fileinfo.file_type == 'transfer_in':
            rows = TransferInRow.objects.filter(fileinfo=fileinfo, state=state)
        elif fileinfo.file_type == 'transfer_out':
            rows = TransferOutRow.objects.filter(fileinfo=fileinfo, state=state)
        elif fileinfo.file_type == 'aliquot':
            rows = AliquotRow.objects.filter(fileinfo=fileinfo, state=state)
        elif fileinfo.file_type == 'test_history':
            rows = DiagnosticTestHistoryRow.objects.filter(fileinfo=fileinfo, state=state)

        response, writer = get_csv_response('file_process_errors_%s.csv' % datetime.today().strftime('%d%b%Y_%H%M'))
        headers = sorted(rows[0].model_to_dict())

        headers.remove("id")
        headers.remove("comment")
        headers.remove("error_message")
        headers.insert(0, 'id')
        headers.append("error_message")
        headers.append('resolve_action')
        headers.append('resolve_date')
        headers.append('assigned_to')
        headers.append('comment')

        writer.writerow(headers)
        
        for row in rows:
            model_dict = model_to_dict(row)
            if model_dict['comment']:
                model_dict['comment'] = row.comment.comment
                model_dict['resolve_action'] = row.comment.resolve_action
                model_dict['resolve_date'] = timezone.get_current_timezone().normalize(row.comment.resolve_date)
                model_dict['assigned_to'] = row.comment.assigned_to
            else:
                model_dict['comment'] = None
                model_dict['resolve_action'] = None
                model_dict['resolve_date'] = None
                model_dict['assigned_to'] = None

            content = [ model_dict[x] for x in headers ]
            writer.writerow(content)

        return response
    except Exception, e:
        logger.exception(e)
        messages.error(request, 'Failed to download file')
        return HttpResponseRedirect(reverse('file_info'))

@login_required
def download_visits_no_subjects(request):
    try:
        rows = Visit.objects.all().exclude(subject__isnull=True)
        response, writer = get_csv_response('visits_no_subjects_%s.csv' % datetime.today().strftime('%d%b%Y_%H%M'))
        headers = model_to_dict(rows[0]).keys()

        writer.writerow(headers)
        
        for row in rows:
            d = model_to_dict(row)
            content = [ d[x] for x in headers ]
            writer.writerow(content)

        return response
    except Exception, e:
        logger.exception(e)
        messages.error(request, 'Failed to download file')

@login_required
def download_subjects_no_visits(request):
    try:
        rows = Subject.objects.filter(visit=None)
        response, writer = get_csv_response('subjects_no_visits_%s.csv' % datetime.today().strftime('%d%b%Y_%H%M'))
        headers = model_to_dict(rows[0]).keys()

        writer.writerow(headers)
        
        for row in rows:
            d = model_to_dict(row)
            content = [ d[x] for x in headers ]
            writer.writerow(content)

        return response
    except Exception, e:
        logger.exception(e)
        messages.error(request, 'Failed to download file')
        return HttpResponseRedirect(reverse('file_info'))

@login_required
@user_passes_test(lambda u: u.is_staff)
def export_file_data(request, file_id=None, state=None):

    try:
        fileinfo = FileInfo.objects.get(pk=file_id)

        if state == 'all':
            state = ['pending',
                     'validated',
                     'imported',
                     'processed',
                     'error']
        else:
            state = ['error']


        if fileinfo.file_type == 'subject':
            rows = SubjectRow.objects.filter(fileinfo__id=file_id, state__in=state)
            headers = ['subject_label',
                       'source_study',
                       'cohort_entry_date_yyyy',
                       'cohort_entry_date_mm',
                       'cohort_entry_date_dd',
                       'country',
                       'cohort_entry_hiv_status',
                       'last_negative_date_yyyy',
                       'last_negative_date_mm',
                       'last_negative_date_dd',
                       'first_positive_date_yyyy',
                       'first_positive_date_mm',
                       'first_positive_date_dd',
                       'fiebig_stage_at_firstpos',
                       'edsc_reported_yyyy',
                       'edsc_reported_mm',
                       'edsc_reported_dd',
                       'ars_onset_date_yyyy',
                       'ars_onset_date_mm',
                       'ars_onset_date_dd',
                       'date_of_birth_yyyy',
                       'date_of_birth_mm',
                       'date_of_birth_dd',
                       'sex',
                       'transgender',
                       'population_group',
                       'risk_sex_with_men',
                       'risk_sex_with_women',
                       'risk_idu',
                       'subtype',
                       'subtype_confirmed',
                       'aids_diagnosis_date_yyyy',
                       'aids_diagnosis_date_mm',
                       'aids_diagnosis_date_dd',
                       'art_initiation_date_yyyy',
                       'art_initiation_date_mm',
                       'art_initiation_date_dd',
                       'art_interruption_date_yyyy',
                       'art_interruption_date_mm',
                       'art_interruption_date_dd',
                       'art_resumption_date_yyyy',
                       'art_resumption_date_mm',
                       'art_resumption_date_dd']
        elif fileinfo.file_type == 'visit':
            rows = VisitRow.objects.filter(fileinfo__id=file_id, state__in=state)
            headers = ['subject_label',
                       'visitdate_yyyy',
                       'visitdate_mm',
                       'visitdate_dd',
                       'visit_hivstatus',
                       'source_study',
                       'cd4_count',
                       'vl',
                       'scopevisit_ec',
                       'pregnant',
                       'hepatitis']
        elif fileinfo.file_type == 'transfer_in':
            rows = TransferInRow.objects.filter(fileinfo__id=file_id, state__in=state)
            headers = ['specimen_label',
                       'subject_label',
                       'drawdate_yyyy',
                       'drawdate_mm',
                       'drawdate_dd',
                       'number_of_containers',
                       'transfer_date_yyyy',
                       'transfer_date_mm',
                       'transfer_date_dd',
                       'location',
                       'transfer_reason',
                       'specimen_type',
                       'volume',
                       'volume_units',
                       'source_study',
                       'notes']
        elif fileinfo.file_type == 'transfer_out':
            rows = TransferOutRow.objects.filter(fileinfo__id=file_id, state__in=state)
            headers = ['specimen_label',
                       'number_of_containers',
                       'specimen_type',
                       'volume',
                       'volume_units',
                       'shipped_in_panel',
                       'shipment_date_yyyy',
                       'shipment_date_mm',
                       'shipment_date_dd',
                       'destination_site']
        elif fileinfo.file_type == 'aliquot':
            rows = AliquotRow.objects.filter(fileinfo__id=file_id, state__in=state)
            headers = ['parent_label',
                       'aliquot_label',
                       'aliquoting_date_yyyy',
                       'aliquoting_date_mm',
                       'aliquoting_date_dd',
                       'specimen_type',
                       'volume',
                       'volume_units',
                       'reason']
        elif fileinfo.file_type == 'test_history':
            rows = DiagnosticTestHistoryRow.objects.filter(fileinfo__id=file_id, state__in=state)
            headers = ['subject',
                       'test_date',
                       'test_code',
                       'test_result',
                       'source',
                       'protocol']

        response, writer = get_csv_response('file_dump_%s.csv' % datetime.today().strftime('%d%b%Y_%H%M'))
        headers.insert(0, 'id')
        headers.append("error_message")
        headers.append('resolve_action')
        headers.append('resolve_date')
        headers.append('assigned_to')
        headers.append('comment')

        writer.writerow(headers)
        
        for row in rows:
            model_dict = model_to_dict(row)
            if row.comment:
                model_dict['comment'] = row.comment.comment
                model_dict['resolve_action'] = row.comment.resolve_action
                model_dict['resolve_date'] = timezone.get_current_timezone().normalize(row.comment.resolve_date)
                model_dict['assigned_to'] = row.comment.assigned_to
            else:
                model_dict['comment'] = None
                model_dict['resolve_action'] = None
                model_dict['resolve_date'] = None
                model_dict['assigned_to'] = None

            content = [ model_dict[x] for x in headers ]
            writer.writerow(content)

        return response
    except Exception, e:
        logger.exception(e)
        messages.error(request, 'Failed to download file')
        return HttpResponseRedirect(reverse('file_info'))

@login_required
@user_passes_test(lambda u: u.is_staff)
def associate_specimen(request, subject_id=None, template="cephia/associate_specimen.html"):
    try:
        if request.method == 'POST':
            if request.POST.has_key('confirm'):
                subject = Subject.objects.get(pk=subject_id)
                specimens = Specimen.objects.filter(visit__isnull=False, subject=subject)
                for spec in specimens:
                    spec.visit_linkage = 'confirmed'
                    spec.save()
            else:
                if request.POST.has_key('provisional'):
                    associate_specimen = Specimen.objects.get(id=request.POST.get('specimen'))
                    associate_visit = Visit.objects.get(id=request.POST.get('visit'))
                    associate_specimen.visit = associate_visit
                    associate_specimen.visit_linkage = 'provisional'
                elif request.POST.has_key('artificial'):
                    associate_specimen = Specimen.objects.get(id=request.POST.get('specimen'))
                    artificial_visit = Visit.objects.create(subject_label=associate_specimen.subject_label,
                                                            subject=associate_specimen.subject,
                                                            visit_date=associate_specimen.reported_draw_date,
                                                            artificial=True)
                    associate_specimen.visit = artificial_visit
                    associate_specimen.visit_linkage = 'provisional'
                elif request.POST.has_key('unlink'):
                    associate_specimen = Specimen.objects.get(id=request.POST.get('unlink'))
                    associate_specimen.visit_linkage = None
                    associate_specimen.visit = None
                associate_specimen.save()
            messages.success(request, 'Successful!')

        context = {}
        subjects = Specimen.objects.values('subject__id').filter(Q(subject__isnull=False) &
                                                                 Q(visit__isnull=True) |
                                                                 Q(visit_linkage='provisional')).distinct()

        context['subjects'] = [ {'subject': Subject.objects.get(pk=x['subject__id']),
                                 'visits': Visit.objects.filter(subject__id=x['subject__id']),
                                 'specimens_with_prov_visits': Specimen.objects.filter(subject__id=x['subject__id'],
                                                                                       visit__isnull=False,
                                                                                       visit_linkage='provisional'),
                                 'specimens_with_visits': Specimen.objects.filter(subject__id=x['subject__id'],
                                                                                  visit__isnull=False,
                                                                                  visit_linkage='confirmed'),
                                 'specimens_without_visits': Specimen.objects.filter(subject__id=x['subject__id'],
                                                                                     visit__isnull=True)} for x in subjects ]

        return render_to_response(template, context, context_instance=RequestContext(request))
    except Exception, e:
        logger.exception(e)
        messages.error(request, 'Failed to make association')
        return HttpResponseRedirect(reverse('specimen'))

@login_required
@user_passes_test(lambda u: u.is_staff)
def row_comment(request, file_type=None, file_id=None, row_id=None, template="cephia/comment_modal.html"):
    try:
        context = {}
        form = RowCommentForm(request.POST or None)
        row = FileInfo.objects.get(id=file_id).get_row(row_id=row_id)
        
        if request.method == "POST":
            if form.is_valid():
                comment = form.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Successfully commented on row')

                row.comment = comment
                row.save()

            url_params = {'file_id':file_id}
            return HttpResponseRedirect(reverse('row_info', kwargs=url_params))
        elif request.method == 'GET':
            if row.comment:
                form = RowCommentForm(initial=row.comment.model_to_dict())
        
            context['comment_form'] = form
            context['data'] = {
                'file_id':file_id,
                'file_type':file_type,
                'row_id':row_id
            }
            response = render_to_response(template, context, context_instance=RequestContext(request))
            return HttpResponse(json.dumps({'response': response.content}))
    except Exception, e:
        logger.exception(e)
        messages.add_message(request, messages.ERROR, 'Failed comment on row')
        return HttpResponseRedirect(reverse('file_info'))



def release_notes(request, template="cephia/release_notes.html"):
    context = {}
    try:
        release_note_lines = {}
        
        raw_release_note_lines = open(os.path.join(settings.PROJECT_HOME, "..", "..", "release_notes.txt")).readlines()
        for line in raw_release_note_lines:
            line = line.strip().lower()
            if line.startswith("#"):
                continue
            if len(line) == 0:
                continue
            name, date, person, description = line.split("|")
            if "issue" in name:
                issue_number = name.strip().replace("issue","")
            else:
                issue_number = None
            release_note_line = {'issue_number': issue_number,
                                 'issue_name': name,
                                 'date': date,
                                 'system': 'cephia',
                                 'person': person,
                                 'description': description}
            if name.startswith('release'):
                release_note_line['type'] = 'release'
                release_note_line['version'] = name
            elif name.startswith('issue'):
                release_note_line['type'] = 'issue'
            else:
                logger.error("Unknown release note type: %s" % name)
                release_note_line['type'] = 'issue'

            release_note_lines.setdefault( date, []).append(release_note_line)

        sorted_release_note_lines = OrderedDict()
        keys = release_note_lines.keys()
        keys.reverse()
        for k in keys:
            sorted_release_note_lines[k] = release_note_lines[k]
            
        context['release_note_lines'] = sorted_release_note_lines
                    
        return render_to_response(template, context, context_instance=RequestContext(request))
    except Exception, ex:
        logger.exception(ex)
        return HttpResponse("Failed to load page: %s" % ex)
