from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib import messages
from cephia.models import Panel
from forms import PanelCaptureForm, PanelFileForm, AssayRunFilterForm
from cephia.forms import FileInfoForm
from assay.models import AssayResult, PanelShipment, PanelMembership, AssayRun
from cephia.models import Assay, Laboratory
import json
from django.utils import timezone
from datetime import datetime
from csv_helper import get_csv_response
from assay_result_factory import *


logger = logging.getLogger(__name__)

@login_required
def panels(request, template="assay/panels.html"):
    context = {}
    panel_capture_form = PanelCaptureForm(request.POST or None)
    panel_file_form = PanelFileForm(request.POST or None)
    upload_form = FileInfoForm(request.POST or None)
    
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

def result_file_upload(request, panel_id=None, template="assay/result_modal.html"):
    context = {}

    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data.__setitem__('priority', 0)
        post_data.__setitem__('file_type', 'assay')
        post_data.__setitem__('panel', panel_id)

        file_info_form = FileInfoForm(post_data, request.FILES)
        if file_info_form.is_valid():
            result_file = file_info_form.save()
            result_file.get_handler().parse()
            result_file.get_handler().validate(panel_id)

            assay_run = AssayRun.objects.create(panel=result_file.panel,
                                                assay=result_file.assay,
                                                laboratory=Laboratory.objects.get(pk=request.POST['laboratory']),
                                                fileinfo=result_file,
                                                run_date=timezone.now())

            result_file.get_handler().process(panel_id, assay_run)
            messages.add_message(request, messages.SUCCESS, 'Successfully uploaded file')
        else:
            messages.add_message(request, messages.ERROR, 'Failed to uploaded file')
        return HttpResponseRedirect(reverse('assay:panels'))
    elif request.method == 'GET':
        form = FileInfoForm()
        context['upload_form'] = form
        context['data'] = {
            'panel_id':panel_id
        }
        response = render_to_response(template, context, context_instance=RequestContext(request))
        return HttpResponse(json.dumps({'response': response.content}))

def panel_memberships(request, panel_id=None, template="assay/panel_memberships.html"):
    context = {}

    if request.method == 'GET':
        context['panel_memberships'] = PanelMembership.objects.filter(panel__id=panel_id)

        return render_to_response(template, context, context_instance=RequestContext(request))

def panel_shipments(request, panel_id=None, template="assay/panel_shipments.html"):
    context = {}

    if request.method == 'GET':
        context['panel_shipments'] = PanelShipment.objects.filter(panel__id=panel_id)

        return render_to_response(template, context, context_instance=RequestContext(request))


def assay_runs(request, panel_id=None, template="assay/assay_runs.html"):
    context = {}
    runs = AssayRun.objects.all()
    if request.method == 'GET':
        form = AssayRunFilterForm(request.GET or None)
        if form.is_valid():
            runs = form.filter()
        context['runs'] = runs
        context['form'] = form
    return render_to_response(template, context, context_instance=RequestContext(request))

def run_results(request, run_id=None, template="assay/run_results.html"):
    context = {}

    if request.method == 'GET':
        if 'csv' in request.GET:
            try:
                first_result = AssayResult.objects.filter(assay_run__id=run_id).first()
                specific_headers, results = first_result.get_specific_results_for_run()
                response, writer = get_csv_response('run_results_%s.csv' % datetime.today().strftime('%d%b%Y_%H%M'))
                headers = list(set(download_common_headers) | set(specific_headers) | set(download_clinical_headers))

                writer.writerow(headers)
                for result in results:
                    import pdb; pdb.set_trace()
                    content = [ result.specimen.specimen_label,
                                result.specimen.id,
                                result.specimen.specimen_label[:4],
                                result.specimen.parent_label,
                                result.specimen.specimen_type.name,
                                result.assay_run.assay.name,
                                result.assay_run.panel.name,
                                result.laboratory.name,
                                result.test_date,
                                result.operator,
                                result.assay_kit_lot,
                                result.plate_identifier,
                                result.specimen_purpose,
                                result.test_mode,
                                result.exclusion,
                                result.warning_msg,
                                result.specimen.source_study.name,
                                result.specimen.visit.visit_date,
                                result.specimen.reported_draw_date,
                                result.specimen.visit.subject.cohort_entry_date,
                                result.specimen.visit.subject.cohort_entry_hiv_status,
                                result.specimen.visit.visit_hivstatus,
                                result.specimen.visit.subject.subtype.name,
                                result.specimen.visit.subject.subtype_confirmed,
                                result.specimen.visit.subject.country.name,
                                result.specimen.visit.subject.sex,
                                'age(vist_date-date_of_birth).years',
                                result.specimen.visit.subject.population_group.name,
                                result.specimen.visit.subject.risk_sex_with_men,
                                result.specimen.visit.subject.risk_sex_with_women,
                                result.specimen.visit.subject.risk_idu,
                                result.specimen.visit.subject.art_initiation_date,
                                result.specimen.visit.subject.aids_diagnosis_date,
                                result.specimen.visit.subject.art_interruption_date,
                                result.specimen.visit.subject.art_resumption_date,
                                result.specimen.visit.treatment_naive,
                                result.specimen.visit.on_treatment,
                                result.specimen.visit.cd4_count,
                                result.specimen.visit.viral_load ]

                    if result.specimen.visit.subject.subject_eddi:
                        content.append(result.specimen.visit.subject.subject_eddi.eddi)
                        content.append(result.specimen.visit.subject.subject_eddi.ep_ddi)
                        content.append(result.specimen.visit.subject.subject_eddi.lp_ddi)
                    if result.specimen.visit.visit_eddi:
                        content.append(result.specimen.visit.visit_eddi.days_since_eddi)
                        content.append(result.specimen.visit.visit_eddi.days_since_ep_ddi)
                        content.append(result.specimen.visit.visit_eddi.days_since_lp_ddi)

                    writer.writerow(content)
                return response
            except Exception, e:
                import pdb; pdb.set_trace()
                logger.exception(e)
                messages.error(request, 'Failed to download file')
        else:
            context['run_results'] = AssayResult.objects.filter(assay_run__id=run_id)
            context['run'] = AssayRun.objects.get(pk=run_id)
            return render_to_response(template, context, context_instance=RequestContext(request))

def specific_results(request, result_id=None, template="assay/specific_results_modal.html"):
    context = {}
    assay_result = AssayResult.objects.get(pk=result_id)

    context['headers'], context['results'] = assay_result.get_specific_results()

    response = render_to_response(template, context, context_instance=RequestContext(request))
    return HttpResponse(json.dumps({'response': response.content}))
