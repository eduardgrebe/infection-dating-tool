from cephia.models import Subject
from diagnostics.models import DiagnosticTestHistory
import logging
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from collections import OrderedDict
from django.utils import timezone
from django.conf import settings


@login_required
def eddi_report(request, template="diagnostics/eddi_report.html"):
    context = {}
    subjects = Subject.objects.all()
    context['subjects'] = subjects
    
    return render_to_response(template, context, context_instance=RequestContext(request))

def subject_test_timeline(request, template="cephia/subject_test_timeline.html"):
    context = {}
    import pdb; pdb.set_trace()
    return render_to_response(template, context, context_instance=RequestContext(request))
