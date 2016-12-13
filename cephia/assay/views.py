from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
import logging
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib import messages
from cephia.models import Panel
from forms import PanelCaptureForm, PanelFileForm, AssayRunFilterForm, AssayRunResultsFilterForm, AssaysByVisitForm, CreateCustomAssayForm

from cephia.forms import FileInfoForm
from assay.models import AssayResult, PanelShipment, PanelMembership, AssayRun
from cephia.models import Assay, Laboratory
import json
from django.utils import timezone
from datetime import datetime
from cephia.csv_helper import get_csv_response
from assay_result_factory import *
from django.core.management import call_command
from tasks import process_file_info
from django.db import transaction
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Permission
from assay_result_factory import register_result_model, register_result_row_model
from cephia.file_handlers.file_handler_register import register_file_handler
from cephia.file_handlers.custom_assay_file_handler import CustomAssayFileHandler
from assay.models import CustomAssayResult
from django.contrib.auth.decorators import user_passes_test
from cephia.views import cephia_login_required

logger = logging.getLogger(__name__)

@cephia_login_required(login_url='users:auth_login')
def panels(request, template="assay/panels.html"):
    context = {}
    panel_capture_form = PanelCaptureForm(request.POST or None)
    panel_file_form = PanelFileForm(request.POST or None)
    upload_form = FileInfoForm(request.POST or None)
    upload_form.filter_options(request)
    
    if request.method == 'POST':
        if panel_capture_form.is_valid():
            panel_capture_form.save()
            
        return HttpResponseRedirect(reverse('assay:panels'))
    elif request.method == 'GET':
        context['panels'] = Panel.objects.all()
        context['panel_capture_form'] = panel_capture_form
        context['panel_file_form'] = panel_file_form
        context['upload_form'] = upload_form
        
        return render_to_response(template, context, context_instance=RequestContext(request))


@cephia_login_required(login_url='users:auth_login')
def shipment_file_upload(request, panel_id=None, template="assay/shipment_modal.html"):
    context = {}

    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data.__setitem__('priority', 0)
        post_data.__setitem__('panel', panel_id)
        post_data.__setitem__('file_type', 'panel_shipment')
        shipment_file_form = PanelFileForm(post_data, request.FILES)
        if shipment_file_form.is_valid():
            shipment_file = shipment_file_form.save()
            shipment_file.get_handler().parse()
            shipment_file.get_handler().validate()
            shipment_file.get_handler().process(panel_id)
            messages.add_message(request, messages.SUCCESS, 'Successfully uploaded file')
        else:
            messages.add_message(request, messages.ERROR, 'Failed to uploaded file')
        return HttpResponseRedirect(reverse('assay:panels'))
    elif request.method == 'GET':
        panel_file_form = PanelFileForm()
        context['panel_file_form'] = panel_file_form
        context['data'] = {
            'panel_id':panel_id
        }
        response = render_to_response(template, context, context_instance=RequestContext(request))
        return HttpResponse(json.dumps({'response': response.content}))


@cephia_login_required(login_url='users:auth_login')
def membership_file_upload(request, panel_id=None, template="assay/membership_modal.html"):
    context = {}

    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data.__setitem__('priority', 0)
        post_data.__setitem__('panel', panel_id)
        post_data.__setitem__('file_type', 'panel_membership')
        membership_file_form = PanelFileForm(post_data, request.FILES)
        if membership_file_form.is_valid():
            membership_file = membership_file_form.save()
            membership_file.get_handler().parse()
            membership_file.get_handler().validate()
            membership_file.get_handler().process(panel_id)
            messages.add_message(request, messages.SUCCESS, 'Successfully uploaded file')
        else:
            messages.add_message(request, messages.ERROR, 'Failed to upload file')
        return HttpResponseRedirect(reverse('assay:panels'))
    elif request.method == 'GET':
        panel_file_form = PanelFileForm()
        context['panel_file_form'] = panel_file_form
        context['data'] = {
            'panel_id':panel_id
        }
        response = render_to_response(template, context, context_instance=RequestContext(request))
        return HttpResponse(json.dumps({'response': response.content}))


@cephia_login_required(login_url='users:auth_login')
def result_file_upload(request, panel_id=None, template="assay/result_modal.html"):
    context = {}

    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data.__setitem__('priority', 0)
        post_data.__setitem__('file_type', 'assay')
        post_data.__setitem__('panel', panel_id)

        file_info_form = FileInfoForm(post_data, request.FILES)
        file_info_form.filter_options(request)

        if file_info_form.is_valid():
            result_file = file_info_form.save()

            
            if settings.PROCESS_TASKS_WITH_CELERY:
                x = lambda: process_file_info.delay(result_file.pk, request.POST['laboratory'])
                transaction.on_commit(x)
            else:
                process_file_info(result_file.pk, request.POST['laboratory'])
            messages.add_message(request, messages.SUCCESS, 'Successfully uploaded file')
        else:
            messages.add_message(request, messages.ERROR, 'Failed to upload file')
        return HttpResponseRedirect(reverse('assay:panels'))
    elif request.method == 'GET':
        form = FileInfoForm()
        form.filter_options(request)
        context['upload_form'] = form
        context['data'] = {
            'panel_id':panel_id
        }
        response = render_to_response(template, context, context_instance=RequestContext(request))
        return HttpResponse(json.dumps({'response': response.content}))


@cephia_login_required(login_url='users:auth_login')
def panel_memberships(request, panel_id=None, template="assay/panel_memberships.html"):
    context = {}

    if request.method == 'GET':
        context['panel_memberships'] = PanelMembership.objects.filter(panel__id=panel_id).order_by('-replicates')

        return render_to_response(template, context, context_instance=RequestContext(request))


@cephia_login_required(login_url='users:auth_login')
def panel_shipments(request, panel_id=None, template="assay/panel_shipments.html"):
    context = {}

    if request.method == 'GET':
        context['panel_shipments'] = PanelShipment.objects.filter(panel__id=panel_id)

        return render_to_response(template, context, context_instance=RequestContext(request))


@cephia_login_required(login_url='users:auth_login')
def assay_runs(request, panel_id=None, template="assay/assay_runs.html"):
    context = {}
    runs = AssayRun.objects.all().order_by('-id')
    preview = AssayResult.objects.all().none().order_by('-id')
    by_visits_form = AssaysByVisitForm(request.POST or None, request.FILES or None)
    form = AssayRunFilterForm(request.GET or None)

    can_purge_runs = False
    permissions = Permission.objects.filter(user=request.user, name='Can purge assay runs')
    if permissions:
        can_purge_runs = True

    if request.method == 'GET' and request.GET:
        if form.is_valid():
            runs = form.filter()

    context['runs'] = runs
    context['form'] = form
    context['can_purge_runs'] = can_purge_runs
    context['by_visits_form'] = by_visits_form

    if request.method == 'POST' and by_visits_form.is_valid():
        return by_visits_form.get_csv_response()
    
    return render_to_response(template, context, context_instance=RequestContext(request))


@cephia_login_required(login_url='users:auth_login')
def preview_assay_runs(request, panel_id=None, template="assay/assay_runs_preview.html"):
    context = {}
    by_visits_form = AssaysByVisitForm(request.GET)

    if by_visits_form.is_valid():
        preview = by_visits_form.preview_filter()

    context['preview'] = preview
    context['by_visits_form'] = by_visits_form

    return render_to_response(template, context, context_instance=RequestContext(request))


@cephia_login_required(login_url='users:auth_login')
def run_results(request, run_id=None, template="assay/run_results.html"):
    context = {}

    if request.method == 'GET':
        if 'csv' in request.GET:
            try:
                first_result = AssayResult.objects.filter(assay_run__id=run_id).first()

                result_model = None
                result_type = ''
                if 'generic' in request.GET:
                    headers, results = first_result.get_results_for_run()
                    result_type = 'generic'
                # this is for wide format download
                # elif 'specific' in request.GET:
                #     headers, results = first_result.get_specific_results_for_run()
                #     result_type = 'specific'
                elif 'detail' in request.GET:
                    headers, results, result_model = first_result.get_detailed_results_for_run()
                    result_type = 'detailed'

                if result_model:
                    download = ResultDownload(headers, results, 'generic' in request.GET, [result_model])
                else:
                    download = ResultDownload(headers, results, 'generic' in request.GET)

                response, writer = get_csv_response('%s_results_run_%s_%s.csv' % (
                    result_type, run_id, datetime.today().strftime('%d%b%Y_%H%M')))

                writer.writerow(download.get_headers())

                for row in download.get_content():
                    writer.writerow(row)

                return response
            except Exception, e:
                messages.error(request, u'Failed to download file: %s' % unicode(e))

        qs = AssayResult.objects.filter(assay_run__id=run_id).order_by('-warning_msg')
        filter_form = AssayRunResultsFilterForm(request.GET or None)
        if filter_form.is_valid():
            qs = filter_form.filter(qs)
        context['filter_form'] = filter_form
        context['run_results'] = qs
        context['run'] = AssayRun.objects.get(pk=run_id)
        return render_to_response(template, context, context_instance=RequestContext(request))


@cephia_login_required(login_url='users:auth_login')
def detailed_run_results(request, run_id=None, template="assay/detailed_run_results.html"):
    context = {}

    filter_form = AssayRunResultsFilterForm(request.GET or None)
    first_result = AssayResult.objects.filter(assay_run__id=run_id).first()
    headers, results, result_model = first_result.get_detailed_results_for_run()
        
    if filter_form.is_valid():
        results = filter_form.filter(results)
        specimen_label = filter_form.cleaned_data['specimen_label']
            
    download = ResultDownload(headers, results, 'generic' in request.GET, [result_model])
    run_results = download.get_content()
    run_headers = download.get_headers()
    result_for_header = AssayResult.objects.filter(assay_run__id=run_id).order_by('-warning_msg').first()

    context['filter_form'] = filter_form
    context['run_results'] = run_results
    context['run_headers'] = run_headers
    context['result_for_header'] = result_for_header
    context['run'] = AssayRun.objects.get(pk=run_id)
    return render_to_response(template, context, context_instance=RequestContext(request))


@cephia_login_required(login_url='users:auth_login')
def specific_results(request, result_id=None, template="assay/specific_results_modal.html"):
    context = {}
    assay_result = AssayResult.objects.get(pk=result_id)

    context['headers'], context['results'] = assay_result.get_specific_results()

    response = render_to_response(template, context, context_instance=RequestContext(request))
    return HttpResponse(json.dumps({'response': response.content}))

def purge_run(request, run_id=None):
    try:
        run = AssayRun.objects.get(pk=run_id)
        AssayResult.objects.filter(assay_run=run).delete()
        get_result_model(run.assay.name).objects.filter(assay_run=run).delete()
        run.delete()
        return HttpResponseRedirect(reverse('assay:assay_runs'))
    except Exception, e:
        logger.exception(e)
        messages.error(request, 'Failed to delete assay run. Please check the log file.')
        return HttpResponseRedirect(request.path)


@cephia_login_required(login_url='users:auth_login')
def custom_assays(request, template="assay/custom_assays.html"):
    context = {}
    custom_assays = Assay.objects.filter(is_custom=True)
    form = CreateCustomAssayForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        instance = form.save(commit=False)
        instance.created_by = request.user
        instance.is_custom = True
        instance.save()
        register_result_model(CustomAssayResult,  instance.name)
        register_result_row_model(CustomAssayResult,  instance.name)
        register_file_handler("assay", CustomAssayFileHandler, instance.name)
        return HttpResponseRedirect(reverse('assay:custom_assays'))

    context['form'] = form
    context['custom_assays'] = custom_assays
    return render_to_response(template, context, context_instance=RequestContext(request))
