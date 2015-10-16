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

logger = logging.getLogger(__name__)

@login_required
def visit_report(request, template="reporting/visit_report.html"):
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
    WHERE (visits.visit_date >= '2009-02-01') AND (specimens.parent_label is NULL)
    GROUP BY visits.id , spectypes.id
    ORDER BY SC_int_size , SubjectLabel , visit_date;
    """

    context['num_rows'] = 1000

    report = Report()
    report.prepare_report(sql, num_rows=context['num_rows'])
    context['report'] = report

    running_row = None
    rolled_rows = []
    for row in report.rows:
        if running_row is None:
            running_row = row
        if running_row['VisitId'] != row['VisitId']:
            rolled_rows.append(running_row)

        num_spec_types = running_row.get('spectypes', 0)
        if num_spec_types == 0:
            report.add_header(row['SpecimenType'])
        running_row[row['SpecimenType']] = num_spec_types+1

    report.set_rows(rolled_rows)
    
    return render_to_response(template, context, context_instance=RequestContext(request))
    