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
from diagnostics.forms import SubjectEDDIFilterForm, SubjectEDDIStatusForm
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms import modelformset_factory

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


@csrf_exempt
@login_required
def eddi_report_detail(request, subject_id=None, template="diagnostics/eddi_report_detail_modal.html"):
    context = {}
    TestHistoryModelFormset = modelformset_factory(DiagnosticTestHistory, fields=('ignore',))
    tests = DiagnosticTestHistory.objects.filter(subject__id=subject_id).order_by('test_date')
    status_form = SubjectEDDIStatusForm(request.POST or None)
    history_formset = TestHistoryModelFormset(request.POST or None, queryset=tests)
    subject = Subject.objects.get(pk=subject_id)

    if request.method == 'POST':
        if status_form.is_valid():
            subject_eddi_status = status_form.save()
            subject.subject_eddi_status = subject_eddi_status
            subject.save()

        if history_formset.is_valid():
            history_formset.save()
            
        data = {
            'success': True,
        }
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')
    elif request.method == 'GET':
        if subject.subject_eddi_status:
            status_form = SubjectEDDIStatusForm(initial=subject.subject_eddi_status.model_to_dict())
        
        context['tests'] = tests
        context['status_form'] = status_form
        context['history_formset'] = history_formset
        context['subject'] = subject

    response = render_to_response(template, context, context_instance=RequestContext(request))
    return HttpResponse(json.dumps({'response': response.content}))
