import logging
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import loader, RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
logger = logging.getLogger(__name__)
from models import Country, FileInfo, SubjectRow, Subject, Ethnicity
from forms import FileInfoForm
from subject_file_handler import SubjectFileHandler
from django.contrib import messages

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
def ethnicity(request, template="cephia/ethnicity.html"):
    context = {}
    ethnicity = Ethnicity.objects.all()
    context['ethnicity'] = ethnicity
    
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def subjects(request, template="cephia/subjects.html"):
    context = {}
    subjects = Subject.objects.all()
    context['subjects'] = subjects
    
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
def row_info(request, file_id, template="cephia/row_info_table.html"):
    context = {}
    fileinfo = FileInfo.objects.get(pk=file_id)
    rows = SubjectRow.objects.filter(fileinfo=fileinfo)
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
        subject_file = FileInfo.objects.get(pk=file_id)
        subject_file_handler = SubjectFileHandler(subject_file)
        success = subject_file_handler.parse()

        if success:
            subject_file.state = 'imported'
            subject_file.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully updated file to status - imported')

        return HttpResponseRedirect(reverse('file_info'))
    except Exception, e:
        messages.add_message(request, messages.ERROR, 'Failed to update file to status - imported')
        return HttpResponseRedirect(reverse('file_info'))


@login_required
def process_file(request, file_id):
    try:
        subject_file = FileInfo.objects.get(pk=file_id)
        subject_file_handler = SubjectFileHandler(subject_file)
        success = subject_file_handler.process()

        if success:
            subject_file.state = 'processed'
            subject_file.save()

        messages.add_message(request, messages.SUCCESS, 'Successfully updated file to status - processed')
        return HttpResponseRedirect(reverse('file_info'))
    except Exception, e:
        messages.add_message(request, messages.ERROR, 'Failed to update file to status - processed')
        return HttpResponseRedirect(reverse('file_info'))


@login_required
def delete_row(request, row_id):
    try:
        import pdb; pdb.set_trace()
        subject_row = SubjectRow.objects.get(pk=row_id)
        messages.add_message(request, messages.SUCCESS, 'Row successfully deleted')

        return HttpResponseRedirect(reverse('file_info'))
    except Exception, e:
        messages.add_message(request, messages.ERROR, 'Could not delete row')
        return HttpResponseRedirect(reverse('file_info'))



