from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from cephia.models import Subject, SubjectEDDI, Visit, VisitEDDI
from diagnostics.models import DiagnosticTestHistory
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update EDDI dates on subjects table'
    args = '<type>'

    def handle(self, *args, **options):
        if args[0] == 'flagged':
            subjects = Subject.objects.filter(subject_eddi__recalculate=True)
            for subject in subjects:
                self._handle_subject(subject.id)
        elif args[0] == 'all':
            subject_ids = DiagnosticTestHistory.objects.values_list('subject_id', flat=True).distinct()
            for subject_id in subject_ids:
                self._handle_subject(subject_id)

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
            _handle_visits(subject_to_udpate)

    def _handle_visits(self, subject):
        visits = Visit.objects.filter(subject=subject)
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

            visit_eddi = VisitEDDI.objects.create(days_since_eddi=days_since_eddi,
                                                  days_since_ep_ddi=days_since_ep_ddi,
                                                  days_since_lp_ddi=days_since_lp_ddi)

            visit.visit_eddi = visit_eddi
            visit.save()

    def cleanup_orphans(self):
        for subject_eddi in SubjectEDDI.objects.all():
            try:
                Subject.objects.get(subject_eddi=subject_eddi):
            except Subject.DoesNotExist:
                subject_eddi.delete()

        for visit_eddi in VisitEDDI.objects.all():
            try:
                Visit.objects.get(visit_eddi=visit_eddi):
            except Visit.DoesNotExist:
                visit_eddi.delete()
