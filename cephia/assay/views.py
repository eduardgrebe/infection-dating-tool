from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib import messages
from models import Panel
from forms import PanelCaptureForm
from cephia.forms import FileInfoForm

logger = logging.getLogger(__name__)

@login_required
def panels(request, template="assay/panels.html"):
    context = {}
    panel_capture_form = PanelCaptureForm(request.POST or None)
    fileinfo_form = FileInfoForm(request.POST or None)
    
    if request.method == 'POST':
        if panel_capture_form.is_valid():
            panel_capture_form.save()
            
        return HttpResponseRedirect(reverse('assay:panels'))
    elif request.method == 'GET':
        context['panels'] = Panel.objects.all()
        context['panel_capture_form'] = panel_capture_form
    
        return render_to_response(template, context, context_instance=RequestContext(request))

def panel_file_upload(request, panel_id=None):
    context = {}
    
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data.__setitem__('priority', 0)
        if 'shipment' in request.POST:
            post_data.__setitem__('file_type', 'panel_shipment')
        elif 'membership' in request.POST:
            post_data.__setitem__('file_type', 'panel_memberships')
            
        fileinfo_form = FileInfoForm(post_data, request.FILES)
        if fileinfo_form.is_valid():
            fileinfo_form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully uploaded file')
        else:
            messages.add_message(request, messages.ERROR, 'Failed to uploaded file')
            
        return HttpResponseRedirect(reverse('assay:panels'))
    elif request.method == 'GET':
        context['panels'] = Panel.objects.all()
        context['fileinfo_form'] = fileinfo_form
    
        return render_to_response(template, context, context_instance=RequestContext(request))
