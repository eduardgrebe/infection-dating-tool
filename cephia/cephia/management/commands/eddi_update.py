from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from cephia.models import Subject, SubjectEDDI, Visit, VisitEDDI
from diagnostics.models import DiagnosticTestHistory, TestPropertyEstimate
from datetime import timedelta
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update EDDI dates on subjects table'
    args = '<type>'

    def handle(self, *args, **options):
        if args[0] == 'flagged':
            subjects = Subject.objects.filter(subject_eddi__recalculate=True)
            with transaction.atomic():
                for subject in subjects:
                    self._handle_subject(subject.id)
        elif args[0] == 'all':
            subject_ids = DiagnosticTestHistory.objects.values_list('subject_id', flat=True).distinct()
            with transaction.atomic():
                for subject_id in subject_ids:
                    self._handle_subject(subject_id)

        self._handle_subjects_without_test_history()
        self.cleanup_orphans()

    def _handle_subject(self, subject_id):
        edsc_days_diff = None
        try:
            lp_ddi = DiagnosticTestHistory.objects.filter(subject__id=subject_id, test_result='Positive', ignore=False).earliest('adjusted_date').adjusted_date
        except DiagnosticTestHistory.DoesNotExist:
            lp_ddi = None

        try:
            ep_ddi = DiagnosticTestHistory.objects.filter(subject__id=subject_id, test_result='Negative', ignore=False).latest('adjusted_date').adjusted_date
        except DiagnosticTestHistory.DoesNotExist:
            ep_ddi = None

        if ep_ddi is None or lp_ddi is None:
            eddi = None
            interval_size = None
        else:
            eddi = ep_ddi + timedelta(days=((lp_ddi - ep_ddi).days / 2))
            interval_size = abs((lp_ddi - ep_ddi).days)

        subject = Subject.objects.get(pk=subject_id)
        if subject.edsc_reported and eddi:
            edsc_days_diff = timedelta(days=(eddi - subject.edsc_reported).days).days

        subject_to_update = Subject.objects.get(pk=subject_id)
        new_eddi = SubjectEDDI.objects.create(ep_ddi=ep_ddi,
                                              lp_ddi=lp_ddi,
                                              interval_size=interval_size,
                                              edsc_days_difference=edsc_days_diff,
                                              eddi=eddi)

        subject_to_update.subject_eddi = new_eddi
        subject_to_update.save()
        if lp_ddi or ep_ddi or eddi:
            self._handle_visits(subject_to_update)

    def _handle_visits(self, subject):
        visits = Visit.objects.filter(subject=subject)

        with transaction.atomic():
            for visit in visits:
                days_since_eddi = None
                days_since_ep_ddi = None
                days_since_lp_ddi = None

                if subject.subject_eddi.eddi:
                    days_since_eddi = timedelta(days=(visit.visit_date - subject.subject_eddi.eddi).days).days

                if subject.subject_eddi.ep_ddi:
                    days_since_ep_ddi = timedelta(days=(visit.visit_date - subject.subject_eddi.ep_ddi).days).days

                if subject.subject_eddi.lp_ddi:
                    days_since_lp_ddi = timedelta(days=(visit.visit_date - subject.subject_eddi.lp_ddi).days).days

                if visit.visit_eddi:
                    visit.visit_eddi.days_since_eddi = days_since_eddi
                    visit.visit_eddi.days_since_ep_ddi = days_since_ep_ddi
                    visit.visit_eddi.days_since_lp_ddi = days_since_lp_ddi

                    visit.visit_eddi.save()
                else:
                    visit_eddi = VisitEDDI.objects.create(days_since_eddi=days_since_eddi,
                                                          days_since_ep_ddi=days_since_ep_ddi,
                                                          days_since_lp_ddi=days_since_lp_ddi)

                    visit.visit_eddi = visit_eddi
                    visit.save()

    def cleanup_orphans(self):
        with transaction.atomic():
            for subject_eddi in SubjectEDDI.objects.all():
                try:
                    subject_count = Subject.objects.get(subject_eddi=subject_eddi)
                except Subject.DoesNotExist:
                    subject_eddi.eddi_type = 'orphaned'
                    subject_eddi.save()


    def _handle_subjects_without_test_history(self):
        subjects = Subject.objects.filter(edsc_reported__isnull=False, subject_eddi__isnull=True)
        mean_diagnostic_delay_days = TestPropertyEstimate.objects.get(test__pk=3, is_default=True).mean_diagnostic_delay_days

        with transaction.atomic():
            for subject in subjects:
                eddi = subject.edsc_reported - timedelta(days=mean_diagnostic_delay_days)
                subject_eddi = SubjectEDDI.objects.create(eddi=eddi,
                                                          recalculate=False,
                                                          eddi_type='edsc_adjusted')
                subject.subject_eddi = subject_eddi
                subject.save()
                self._handle_visits(subject)
