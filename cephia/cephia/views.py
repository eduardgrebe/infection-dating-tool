import logging
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import loader, RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from file_handlers import SubjectFileHandler, VisitFileHandler
from models import Country, FileInfo, SubjectRow, Subject, Ethnicity, Visit, VisitRow
from forms import FileInfoForm
from django.contrib import messages

logger = logging.getLogger(__name__)


@login_required
def home(request, template="cephia/home.html"):
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
def sources(request, template="cephia/sources.html"):
    context = {}
    sources = Source.objects.all()
    context['sources'] = sources
    
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def subjects(request, template="cephia/subjects.html"):
    context = {}
    subjects = Subject.objects.all()
    context['subjects'] = subjects
    
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def visits(request, template="cephia/visits.html"):
    context = {}
    visits = Visit.objects.all()
    context['visits'] = visits
    
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def file_info(request, template="cephia/file_info.html"):
    if request.method == "GET":
        context = {}
        files = FileInfo.objects.all()
        form = FileInfoForm()
        context['files'] = files
        context['form'] = form
        
        return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def row_info(request, file_id, template=None):
    context = {}
    fileinfo = FileInfo.objects.get(pk=file_id)

    if fileinfo.file_type == 'subject':
        rows = SubjectRow.objects.filter(fileinfo=fileinfo)
        template = 'cephia/subject_row_info.html'
    elif fileinfo.file_type == 'visit':
        rows = VisitRow.objects.filter(fileinfo=fileinfo)
        template = 'cephia/visit_row_info.html'

    context['rows'] = rows
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
        message.error(request, 'Failed to download file')
        return HttpResponseRedirect(reverse('file_info'))

@login_required
def upload_file(request):
    try:
        if request.method == "POST":
            form = FileInfoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save();
                messages.add_message(request, messages.SUCCESS, 'Successfully uploaded file')
                return HttpResponseRedirect(reverse('file_info'))

    except Exception, e:
        messages.add_message(request, messages.ERROR, 'Failed to upload file')
        return HttpResponseRedirect(reverse('file_info'))


@login_required
def parse_file(request, file_id):
    try:
        file_to_parse = FileInfo.objects.get(pk=file_id)

        if file_to_parse.file_type == 'subject':
            file_handler = SubjectFileHandler(file_to_parse)
        elif file_to_parse.file_type == 'visit':
            file_handler = VisitFileHandler(file_to_parse)

        num_rows_parsed = file_handler.parse()

        file_to_parse.state = 'imported'
        file_to_parse.save()
        messages.add_message(request, messages.SUCCESS, 'Successfully imported ' + str(num_rows_parsed) + ' rows ')

        return HttpResponseRedirect(reverse('file_info'))
    except Exception, e:
        messages.add_message(request, messages.ERROR, 'Import failed!')
        return HttpResponseRedirect(reverse('file_info'))


@login_required
def process_file(request, file_id):
    try:
        file_to_parse = FileInfo.objects.get(pk=file_id)

        if file_to_parse.file_type == 'subject':
            file_handler = SubjectFileHandler(file_to_parse)
        elif file_to_parse.file_type == 'visit':
            file_handler = SubjectFileHandler(file_to_parse)
        
        num_rows_processed = file_handler.process()

        file_to_parse.state = 'processed'
        file_to_parse.save()
        messages.add_message(request, messages.SUCCESS, 'Successfully processed ' + str(num_rows_processed) + ' rows ')

        return HttpResponseRedirect(reverse('file_info'))
    except Exception, e:
        import pdb; pdb.set_trace()
        messages.add_message(request, messages.ERROR, 'Failed to update file to status - processed')
        return HttpResponseRedirect(reverse('file_info'))


@login_required
def delete_row(request, row_id):
    try:
        subject_row = SubjectRow.objects.get(pk=row_id)
        messages.add_message(request, messages.SUCCESS, 'Row successfully deleted')

        return HttpResponseRedirect(reverse('file_info'))
    except Exception, e:
        messages.add_message(request, messages.ERROR, 'Could not delete row')
        return HttpResponseRedirect(reverse('file_info'))



