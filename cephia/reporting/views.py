import logging
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from report_helper import Report
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from csv_helper import get_csv_response
from datetime import datetime, timedelta
import json
from collections import defaultdict, OrderedDict
from django.utils import timezone
from cephia.csv_helper import get_csv_response
from cephia.models import Specimen
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from reporting.forms import VisitReportFilterForm, GenericReportFilterForm

logger = logging.getLogger(__name__)

@login_required
def visit_material(request, template="reporting/visit_material.html"):
    context = {}

    sql = """
    SELECT
    subjects.id AS SubjectId ,
    visits.id AS VisitId ,
    subjects.subject_label AS SubjectLabel,
    visits.visit_date AS VisitDate,
    subjects.cohort_entry_date AS EntryDate ,
    subjects.cohort_entry_hiv_status AS EntryStatus ,
    subjects.last_negative_date AS LNDate ,
    subjects.first_positive_date AS FPDate ,
    ABS(DATEDIFF(subjects.last_negative_date,subjects.first_positive_date)) AS SC_int_size ,
    DATE_ADD(subjects.last_negative_date, INTERVAL (ABS(DATEDIFF(subjects.last_negative_date,subjects.first_positive_date)) / 2) DAY) AS SC_int_midpoint,
    TRUNCATE(DATEDIFF(visits.visit_date,subjects.first_positive_date)+(ABS(DATEDIFF(subjects.last_negative_date,subjects.first_positive_date))/2), 0) AS DaysSinceSCi_mp,
    DATEDIFF(visits.visit_date,subjects.last_negative_date) AS DaysSinceLN,
    DATEDIFF(visits.visit_date,subjects.first_positive_date) AS DaysSinceFP ,
    DATEDIFF(visits.visit_date,subjects.cohort_entry_date) AS DaysSinceEntry ,
    subtypes.name as subtype,
    subjects.subtype_confirmed as st_conf,
    spectypes.name AS SpecimenType,
    COUNT(specimens.id) AS n_specs ,
    SUM(specimens.initial_claimed_volume) AS vol_recd ,
    specimens.volume_units
    FROM cephia_subjects AS subjects 
    INNER JOIN cephia_visits AS visits ON subjects.id = visits.subject_id
    INNER JOIN cephia_specimens AS specimens ON visits.id = specimens.visit_id
    INNER JOIN cephia_specimen_types AS spectypes ON specimens.specimen_type_id = spectypes.id
    LEFT JOIN cephia_subtypes AS subtypes ON subjects.subtype_id = subtypes.id
    WHERE (visits.visit_date >= 'MIN_DATE') AND (specimens.parent_label is NULL)
    GROUP BY visits.id , spectypes.id
    ORDER BY SC_int_size DESC, SubjectLabel , visit_date;
    """

    filter_form = VisitReportFilterForm(request.GET or None)
    if filter_form.is_valid():
        min_date = filter_form.cleaned_data['visit_date'].strftime('%Y-%m-%d')
    else:
        min_date = '2013-02-01'
    sql = sql.replace("MIN_DATE", min_date)
    
    as_csv = request.GET.get('csv', False)
    if not as_csv:
        context['num_rows'] = 1000
    else:
        context['num_rows'] = None

    report = Report()
    report.prepare_report(sql, num_rows=context['num_rows'])
    context['report'] = report
    context['filter_form'] = filter_form

    report.remove_header('SpecimenType')
    report.remove_header('vol_recd')
    report.remove_header('volume_units')

    specimen_type_headers = []
    
    running_row = None
    rolled_rows = []
    for row in report.rows:
        if running_row is None:
            running_row = row
        if running_row['VisitId'] != row['VisitId']:
            del running_row['SpecimenType']
            del running_row['vol_recd']
            del running_row['volume_units']
            rolled_rows.append(running_row)
            running_row = row

        header_name = "Number of %s" % row['SpecimenType']
        vol_header_name = "Volume of %s" % row['SpecimenType']
        vol_units_header_name = "Units of %s" % row['SpecimenType']
        num_spec_types = running_row.get('spectypes', 0)
        if num_spec_types == 0:
            report.add_header(header_name)
            report.add_header(vol_header_name)
            report.add_header(vol_units_header_name)

        vol = running_row.get(vol_header_name, 0)
        vol += row['vol_recd'] or 0
            
        running_row[header_name] = num_spec_types+1
        running_row[vol_header_name] = vol
        running_row[vol_units_header_name] = row['volume_units']
        
    report.set_rows(rolled_rows)

    if as_csv:
        response, writer = get_csv_response("VisitReport_%s.csv" % datetime.today().strftime("%D%b%Y_%H%M"))
        writer.writerow(report.headers)
        for row in report.rows:
            writer.writerow( [ row.get(x, None) for x in report.headers ] )
        return response
    
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def all_subject_material(request, template="reporting/all_subject_material.html"):
    context = {}

    sql = """
    SELECT
    subjects.id AS SubjectId ,
    visits.id AS VisitId ,
    subjects.subject_label AS SubjectLabel,
    visits.visit_date AS VisitDate,
    subjects.cohort_entry_date AS EntryDate ,
    subjects.cohort_entry_hiv_status AS EntryStatus ,
    subjects.last_negative_date AS LNDate ,
    subjects.first_positive_date AS FPDate ,
    ABS(DATEDIFF(subjects.last_negative_date,subjects.first_positive_date)) AS SC_int_size ,
    DATEDIFF(visits.visit_date,subjects.first_positive_date)+(ABS(DATEDIFF(subjects.last_negative_date,subjects.first_positive_date))/2) AS DaysSinceEDDI ,
    DATEDIFF(visits.visit_date,subjects.first_positive_date) AS DaysSinceFP ,
    DATEDIFF(visits.visit_date,subjects.cohort_entry_date) AS DaysSinceEntry ,
    spectypes.name AS SpecimenType,
    COUNT(specimens.id) AS n_specs ,
    SUM(specimens.initial_claimed_volume) AS vol_recd ,
    specimens.volume_units
    FROM cephia_subjects AS subjects 
    INNER JOIN cephia_visits AS visits ON subjects.id = visits.subject_id
    INNER JOIN cephia_specimens AS specimens ON visits.id = specimens.visit_id
    INNER JOIN cephia_specimen_types AS spectypes ON specimens.specimen_type_id = spectypes.id
    WHERE (visits.visit_date >= 'MIN_DATE') AND (specimens.parent_label is NULL)
    GROUP BY visits.id , spectypes.id
    ORDER BY SC_int_size , SubjectLabel , visit_date;
    """

    filter_form = VisitReportFilterForm(request.GET or None)
    if filter_form.is_valid():
        min_date = filter_form.cleaned_data['visit_date'].strftime('%Y-%m-%d')
    else:
        min_date = '2013-02-01'
    sql = sql.replace("MIN_DATE", min_date)
    
    as_csv = request.GET.get('csv', False)
    if not as_csv:
        context['num_rows'] = 1000
    else:
        context['num_rows'] = None

    report = Report()
    report.prepare_report(sql, num_rows=context['num_rows'])
    context['report'] = report
    context['filter_form'] = filter_form

    report.remove_header('SpecimenType')
    report.remove_header('vol_recd')
    report.remove_header('volume_units')

    specimen_type_headers = []
    
    running_row = None
    rolled_rows = []
    for row in report.rows:
        if running_row is None:
            running_row = row
        if running_row['VisitId'] != row['VisitId']:
            del running_row['SpecimenType']
            del running_row['vol_recd']
            del running_row['volume_units']
            rolled_rows.append(running_row)
            running_row = row

        header_name = "Number of %s" % row['SpecimenType']
        vol_header_name = "Volume of %s" % row['SpecimenType']
        vol_units_header_name = "Units of %s" % row['SpecimenType']
        num_spec_types = running_row.get('spectypes', 0)
        if num_spec_types == 0:
            report.add_header(header_name)
            report.add_header(vol_header_name)
            report.add_header(vol_units_header_name)

        vol = running_row.get(vol_header_name, 0)
        vol += row['vol_recd'] or 0
            
        running_row[header_name] = num_spec_types+1
        running_row[vol_header_name] = vol
        running_row[vol_units_header_name] = row['volume_units']
        
    report.set_rows(rolled_rows)

    if as_csv:
        response, writer = get_csv_response("VisitReport_%s.csv" % datetime.today().strftime("%D%b%Y_%H%M"))
        writer.writerow(report.headers)
        for row in report.rows:
            writer.writerow( [ row.get(x, None) for x in report.headers ] )
        return response
    
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def generic_report(request, template="reporting/generic_report.html"):
    context = {}
    query_form = GenericReportFilterForm(request.POST or None)
    save = request.GET.get('saved', None)
    as_csv = request.GET.get('csv', False)
    import pdb; pdb.set_trace()
    if query_form.is_valid():
        if save:
            query_form.save()
            template = "reporting/report_landing_page.html"
            return render_to_response(template, context, context_instance=RequestContext(request))

        sql = query_form.cleaned_data['query']
    else:
        sql = None

    context['query_form'] = query_form

    if not as_csv:
        context['num_rows'] = 1000
    else:
        context['num_rows'] = None

    if sql:
        report = Report()
        report.prepare_report(sql, num_rows=context['num_rows'])
        context['report'] = report
    
    if as_csv:
        response, writer = get_csv_response("GenericReport_%s.csv" % datetime.today().strftime("%D%b%Y_%H%M"))
        writer.writerow(report.headers)
        for row in report.rows:
            writer.writerow( [ row.get(x, None) for x in report.headers ] )
        return response
    
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def report_landing_page(request, template="reporting/report_landing_page.html"):
    context = {}

    return render_to_response(template, context, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def visit_specimen_report(request, template="reporting/visit_specimen_modal.html"):
    context = {}
    import pdb; pdb.set_trace()
    visit_ids = request.POST.getlist('VisitId', None)
    subject_ids = request.POST.getlist('SubjectId', None)
                              
    if visit_ids and subject_ids:
        specimens = Specimen.objects.filter(Q(visit__id__in=visit_ids) | Q(subject__id__in=subject_ids))
    elif subject_ids and not visit_ids:
        specimens = Specimen.objects.filter(subject__id__in=subject_ids)
    elif visit_ids and not subject_ids:
        specimens = Specimen.objects.filter(visit__id__in=visit_ids)
    else:
        specimens = None

    context['specimens'] = specimens
    
    response = render_to_response(template, context, context_instance=RequestContext(request))
    return HttpResponse(json.dumps({'response': response.content}))


@csrf_exempt
@login_required
def visit_specimen_report_download(request):
    context = {}

    # GET a preset list of ids from somewhere
    visit_ids = request.POST.getlist('VisitId', None)
    subject_ids = request.POST.getlist('SubjectId', None)
                              
    if visit_ids and subject_ids:
        specimens = Specimen.objects.filter(Q(visit__id__in=visit_ids) | Q(subject__id__in=subject_ids))
    elif subject_ids and not visit_ids:
        specimens = Specimen.objects.filter(subject__id__in=subject_ids)
    elif visit_ids and not subject_ids:
        specimens = Specimen.objects.filter(visit__id__in=visit_ids)
    else:
        specimens = None

    context['specimens'] = specimens

    response, writer = get_csv_response('visit_specimens_%s.csv' % datetime.today().strftime('%d%b%Y_%H%M'))
    headers = ['VisitId','SubjectId','SpecimenId','SpecimenLabel','VolumeUnits','InitialVolume','VolumeRemaining']
    for specimen in specimens:
        writer.writerow( [ specimen.visit.id,
                           specimen.subject.id,
                           specimen.id,
                           specimen.specimen_label,
                           specimen.volume_units,
                           specimen.initial_claimed_volume,
                           specimen.volume] )
    return response
