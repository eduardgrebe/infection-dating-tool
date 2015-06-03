import logging
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import loader, RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
logger = logging.getLogger(__name__)
from models import Country, FileInfo
from forms import FileInfoForm

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
def file_info(request, template="cephia/file_info.html"):
    if request.method == "GET":
        context = {}
        files = FileInfo.objects.all()
        form = FileInfoForm()
        context['files'] = files
        context['form'] = form
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
        return HttpResponse({'success':False, 'message':'Failed to download file'})

@login_required
def upload_file(request):
    try:
        if request.method == "POST":
            form = FileInfoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save();
                return HttpResponseRedirect(reverse('file_info'))
    except Exception, e:
        return HttpResponse({'success':False, 'message':'Failed to upload file'})

@login_required
def manually_parse_file(request):
    if request.method == "POST":
        try:
            file_id = request.POST['file_id']
            file = FileInfo.objects.get(pk=file_id)
            file.state = 'IM'
            file.save()
            return HttpResponse({'success':True, 'message':'Successfully updated file to status - imported'})
        except Exception, e:
            return HttpResponse({'success':False, 'message':'Failed to update file to status - imported'})

