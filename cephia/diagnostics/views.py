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
from diagnostics.forms import SubjectEDDIFilterForm

@login_required
def eddi_report(request, template="diagnostics/eddi_report.html"):
    context = {}
    subjects = Subject.objects.all()

    form = SubjectEDDIFilterForm(request.GET or None)
    if form.is_valid():
        subjects = form.filter(subjects)

    context['subjects'] = subjects
    context['form'] = form
    
    return render_to_response(template, context, context_instance=RequestContext(request))


#@csrf_exempt
@login_required
def eddi_report_detail(request, template="diagnostics/eddi_report_detail_modal.html"):
    context = {}
    import pdb; pdb.set_trace()
    subject_ids = request.POST.getlist('SubjectId', None)
    specimens = Specimen.objects.filter(Q(visit__id__in=visit_ids) | Q(subject__id__in=subject_ids))

    context['specimens'] = specimens
    response = render_to_response(template, context, context_instance=RequestContext(request))
    return HttpResponse(json.dumps({'response': response.content}))
