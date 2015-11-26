from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib import messages
from models import Panel
from forms import PanelCaptureForm

logger = logging.getLogger(__name__)

@login_required
def panels(request, template="assay/panels.html"):
    context = {}
    panel_capture_form = PanelCaptureForm(request.POST or None)
    
    if request.method == 'POST':
        if panel_capture_form.is_valid():
            panel_capture_form.save()
            
        return HttpResponseRedirect(reverse('assay:panels'))
    elif request.method == 'GET':
        context['panels'] = Panel.objects.all()
        context['panel_capture_form'] = panel_capture_form
    
        return render_to_response(template, context, context_instance=RequestContext(request))
