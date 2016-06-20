from django.core.management.base import BaseCommand, CommandError
from cephia.models import Visit, VisitCalculation
from django.db.models import Q, F
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Perform calculations on visits and populate visit detail table'

    def handle(self, *args, **options):
        with transaction.atomic():
            all_subjects = Subject.objects.all()
            all_subject_visits = Visit.objects.filter(subject=subject)
            for visit in all_subject_visits:
                age = visit.visit_date - visit.subject.date_of_birth
                time_since_cohort_entry = visit_date - cohort_entry_date
                time_since_first_draw = visit_date - earliest visit_date
                time_since_first_art = None
                time_from_eddi_to_tx = None
                after_aids_diagnosis = False
                ever_aids_diagnosis = False
                ever_scope_ec = False

                if visit.visit_date > visit.subject.aids_diagnosis_date and visit.subject.aids_diagnosis_date:
                    after_aids_diagnosis = True

                if visit.subject.aids_diagnosis_date:
                    ever_aids_diagnosis = True

                if visit.subject.on_treatment:
                    time_since_first_art = visit.visit_date - visit.subject.art_initiation_date

                if on_treatment and first_treatment:
                    time_since_current_art_init = "Do something here"

                if not visit.treatment_naive and visit.subject.subject_eddi.eddi:
                    days_from_eddi_to_first_art = then art_initiation_date - eddi

                has_scope_ec = [ x for x in all_subject_visits if x.scopevisit_ec ]
                if has_scope_ec:
                    ever_scope_ec = True

                earliest_visit_date = earliest visit date for subject
