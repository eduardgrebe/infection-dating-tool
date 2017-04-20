# from cephia.models import Subject
# from diagnostics.models import DiagnosticTestHistory, TestPropertyEstimate
# import logging
# from django.shortcuts import render_to_response
# from django.http import HttpResponseRedirect, HttpResponse
# from django.core.urlresolvers import reverse
# from django.template import RequestContext
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.forms.models import model_to_dict
# from cephia.csv_helper import get_csv_response
# from datetime import datetime
# from collections import OrderedDict
# from django.utils import timezone
# from django.conf import settings
# from diagnostics.forms import SubjectEDDIFilterForm, SubjectEDDIStatusForm
# from django.views.decorators.csrf import csrf_exempt
# import json
# from django.forms import modelformset_factory
# from django.core.management import call_command
# from django.contrib.auth.decorators import user_passes_test
# from cephia.views import cephia_login_required

# logger = logging.getLogger(__name__)

# @cephia_login_required(login_url='users:auth_login')
# def eddi_report(request, template="diagnostics/eddi_report.html"):
#     context = {}
#     subjects = Subject.objects.all()

#     form = SubjectEDDIFilterForm(request.GET or None)
#     if form.is_valid():
#         subjects = form.filter(subjects)

#     context['subjects'] = subjects
#     context['form'] = form

#     if 'csv' in request.GET:
#         try:
#             response, writer = get_csv_response('eddi_report_%s.csv' % datetime.today().strftime('%d%b%Y_%H%M'))
#             headers = ['subject',
#                        'ep ddi',
#                        'lp ddi',
#                        'interval size',
#                        'eddi',
#                        'cohort entry',
#                        'entry status',
#                        'reported ln',
#                        'reported fp',
#                        'reported edsc',
#                        'eddi status']

#             writer.writerow(headers)
#             for subject in subjects:
#                 writer.writerow( [ subject.subject_label,
#                                    subject.subject_eddi.ep_ddi if subject.subject_eddi else None,
#                                    subject.subject_eddi.lp_ddi if subject.subject_eddi else None,
#                                    subject.subject_eddi.interval_size if subject.subject_eddi else None,
#                                    subject.subject_eddi.eddi if subject.subject_eddi else None,
#                                    subject.cohort_entry_date,
#                                    subject.cohort_entry_hiv_status,
#                                    subject.last_negative_date,
#                                    subject.first_positive_date,
#                                    subject.edsc_reported,
#                                    subject.subject_eddi_status.status if subject.subject_eddi_status else None ] )
#             return response
#         except Exception, e:
#             logger.exception(e)
#             messages.error(request, 'Failed to download file')

#     return render_to_response(template, context, context_instance=RequestContext(request))


# @cephia_login_required(login_url='users:auth_login')
# def subject_test_timeline(request, subject_id=None, template="cephia/subject_test_timeline.html"):
#     context = {}
#     context['subject_id'] = subject_id
#     return render_to_response(template, context, context_instance=RequestContext(request))


# @cephia_login_required(login_url='users:auth_login')
# def subject_timeline_data(request, subject_id=None, template="diagnostics/timeline_data.json"):
#     context = {}
#     context['tests'] = DiagnosticTestHistory.objects.filter(subject__id=subject_id, ignore=False)
#     context['subject'] = Subject.objects.get(pk=subject_id)
#     response = render_to_response(template, context, context_instance=RequestContext(request))
#     return HttpResponse(json.dumps({'response': response.content}))


# @csrf_exempt
# @cephia_login_required(login_url='users:auth_login')
# def eddi_report_detail(request, subject_id=None, template="diagnostics/eddi_report_detail_modal.html"):
#     context = {}
#     TestHistoryModelFormset = modelformset_factory(DiagnosticTestHistory, fields=('ignore',))
#     tests = DiagnosticTestHistory.objects.filter(subject__id=subject_id).order_by('test_date')
#     status_form = SubjectEDDIStatusForm(request.POST or None)
#     history_formset = TestHistoryModelFormset(request.POST or None, queryset=tests)
#     subject = Subject.objects.get(pk=subject_id)
#     default_test_properties = { testimate.test.id: testimate.estimate_label for testimate in TestPropertyEstimate.objects.filter(is_default=True) }

#     if request.method == 'POST':
#         if status_form.is_valid():
#             subject_eddi_status = status_form.save()
#             subject.subject_eddi_status = subject_eddi_status
#             subject.save()

#         if history_formset.is_valid():
#             history_formset.save()
#             subject.subject_eddi.recalculate = True
#             subject.subject_eddi.save()
            
#         data = {
#             'success': True,
#         }
#         json_data = json.dumps(data)
#         return HttpResponse(json_data, content_type='application/json')
#     elif request.method == 'GET':
#         if subject.subject_eddi_status:
#             status_form = SubjectEDDIStatusForm(initial=subject.subject_eddi_status.model_to_dict())
        
#         context['tests'] = tests
#         context['status_form'] = status_form
#         context['history_formset'] = history_formset
#         context['subject'] = subject
#         context['test_properties'] = default_test_properties

#     response = render_to_response(template, context, context_instance=RequestContext(request))
#     return HttpResponse(json.dumps({'response': response.content}))


# def recalculate_eddi(request):
#     call_command('eddi_update', 'flagged')
#     return HttpResponseRedirect(reverse('diagnostics:eddi_report'))
