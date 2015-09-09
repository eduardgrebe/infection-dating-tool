import logging
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from models import (Country, FileInfo, SubjectRow, Subject, Ethnicity, Visit,
                    VisitRow, Site, Specimen, SpecimenType, TransferInRow,
                    Study, TransferOutRow, AliquotRow)
from forms import (FileInfoForm, RowCommentForm, SubjectFilterForm,
                   VisitFilterForm, RowFilterForm, SpecimenFilterForm,
                   FileInfoFilterForm)
from django.forms.models import model_to_dict
from csv_helper import get_csv_response
from datetime import datetime, timedelta
import json
from collections import defaultdict

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
def table_management(request, template="cephia/tms_home.html"):
    context = {}
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def countries(request, template="cephia/countries.html"):
    context = {}
    countries = Country.objects.all().order_by("name")
    context['countries'] = countries
    
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def ethnicities(request, template="cephia/ethnicities.html"):
    context = {}
    ethnicities = Ethnicity.objects.all()
    context['ethnicities'] = ethnicities
    
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def studies(request, template="cephia/studies.html"):
    context = {}
    studies = Study.objects.all()
    context['studies'] = studies
    
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def sites(request, template="cephia/sites.html"):
    context = {}
    sites = Site.objects.all()
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
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def visits(request, template="cephia/visits.html"):
    context = {}
    visits = Visit.objects.all()

    form = VisitFilterForm(request.GET or None)
    if form.is_valid():
        visits = form.filter(visits)

    context['visits'] = visits
    context['form'] = form
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
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def specimen_type(request, template="cephia/specimen_type.html"):
    context = {}
    spec_type = SpecimenType.objects.all()
    context['spec_type'] = spec_type
    
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def file_info(request, template="cephia/file_info.html"):
    context = {}

    if request.method == "GET":
        upload_form = FileInfoForm()
        filter_form = FileInfoFilterForm(request.GET or None)
        if filter_form.is_valid():
            files = filter_form.filter()
        else:
            files = FileInfo.objects.all().order_by('-created')

        context['files'] = files
        context['upload_form'] = upload_form
        context['filter_form'] = filter_form
        
    return render_to_response(template, context, context_instance=RequestContext(request))

   
@login_required
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
def upload_file(request):
    try:
        FILE_PRIORITIES = {
            'subject': 1,
            'visit': 2,
            'transfer_in': 3,
            'aliquot': 4,
            'transfer_out': 5
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
            if form.is_valid():
                form.save();
                messages.add_message(request, messages.SUCCESS, 'Successfully uploaded file')
            else:
                messages.add_message(request, messages.ERROR, 'Failed to uploaded file')
    
            return HttpResponseRedirect(reverse('file_info'))

    except Exception, e:
        logger.exception(e)
        messages.add_message(request, messages.ERROR, 'Failed to upload file')
        return HttpResponseRedirect(reverse('file_info'))


@login_required
def parse_file(request, file_id):
    try:
        file_to_parse = FileInfo.objects.get(pk=file_id)
        file_handler = file_to_parse.get_handler()
        msg = file_handler.validate_file()

        if msg:
            messages.add_message(request, messages.WARNING, msg)

        num_success, num_fail = file_handler.parse()
        
        if num_fail > 0:
            messages.add_message(request, messages.ERROR, 'Failed to import ' + str(num_fail) + ' rows. ')
        else:
            file_to_parse.state = 'imported'
            file_to_parse.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully imported ' + str(num_success) + ' rows. ')
    
        return HttpResponseRedirect(reverse('file_info'))
    except Exception, e:
        logger.exception(e)
        messages.add_message(request, messages.ERROR, 'Import failed: ' + e.message)
        file_to_parse.state = 'file_error'
        file_to_parse.message = e.message
        file_to_parse.save()
        return HttpResponseRedirect(reverse('file_info'))

@login_required
def validate_rows(request, file_id):
    try:
        file_to_validate = FileInfo.objects.get(pk=file_id)
        file_handler = file_to_validate.get_handler()

        num_success, num_fail = file_handler.validate()

        fail_msg = 'Failed to validate ' + str(num_fail) + ' rows. '
        msg = 'Successfully validated ' + str(num_success) + ' rows. '

        if num_fail > 0:
            file_to_validate.state = 'row_error'
        else:
            file_to_validate.state = 'validated'

        file_to_validate.message = fail_msg + ' ' + msg
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
def process_file(request, file_id):
    try:
        file_to_process = FileInfo.objects.get(pk=file_id)
        file_handler = file_to_process.get_handler()
        
        num_success, num_fail = file_handler.process()

        fail_msg = 'Failed to process ' + str(num_fail) + ' rows. '
        msg = 'Successfully processed ' + str(num_success) + ' rows. '

        if num_fail > 0:
            messages.add_message(request, messages.WARNING, fail_msg)
            file_to_process.state = 'error'
        else:
            file_to_process.state = 'processed'
    
        messages.add_message(request, messages.SUCCESS, msg)

        file_to_process.message = fail_msg + ' ' + msg
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

        response, writer = get_csv_response('file_process_errors_%s.csv' % datetime.today().strftime('%d%b%Y_%H%M'))
        headers = rows[0].model_to_dict().keys()

        headers.append('resolve_action')
        headers.append('resolve_date')
        headers.append('assigned_to')

        writer.writerow(headers)
        
        for row in rows:
            model_dict = model_to_dict(row)
            if model_dict['comment']:
                model_dict['comment'] = row.comment.comment
                model_dict['resolve_action'] = row.comment.resolve_action
                model_dict['resolve_date'] = row.comment.resolve_date
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
        return HttpResponseRedirect(reverse('file_info'))

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
def associate_specimen(request, specimen_id=None, template="cephia/associate_specimen.html"):
    try:
        if request.method == 'POST':
            associate_specimen = Specimen.objects.get(id=specimen_id)
            associate_visit = Visit.objects.get(id=request.POST.get('visit'))
            associate_specimen.visit = associate_visit
            associate_specimen.save()
            messages.success(request, 'Successfully associated specimen with visit')

        context = {}
        subjects = Specimen.objects.values('subject__id').filter(subject__isnull=False).distinct()

        context['subjects'] = [ {'subject': Subject.objects.get(pk=x['subject__id']),
                                 'visits': Visit.objects.filter(subject__id=x['subject__id']),
                                 'specimens': Specimen.objects.filter(subject__id=x['subject__id'])} for x in subjects ]

        [ x['visits'] for x in context['subjects'] ]

        return render_to_response(template, context, context_instance=RequestContext(request))
    except Exception, e:
        logger.exception(e)
        messages.error(request, 'Failed to make association')
        return HttpResponseRedirect(reverse('specimen'))

@login_required
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

@login_required
def artificial_visit(request, specimen_id=None):
    try:
        associate_specimen = Specimen.objects.get(id=specimen_id)
        associate_visit = Visit.objects.create(subject_label='Artificial_' + associate_specimen.specimen_label,
                                               visit_date=associate_specimen.reported_draw_date,
                                               artificial=True)
        associate_specimen.visit = associate_visit
        associate_specimen.save()
        messages.success(request, 'Successfully created artificial visit')

        return HttpResponseRedirect(reverse('associate_specimen'))
    except Exception, e:
        logger.exception(e)
        messages.error(request, 'Failed to create artificial visit')
        return HttpResponseRedirect(reverse('associate_specimen'))
