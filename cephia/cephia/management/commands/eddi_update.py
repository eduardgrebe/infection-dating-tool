from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from cephia.models import Subject, SubjectEDDI
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
            tci_end = DiagnosticTestHistory.objects.filter(subject__id=subject_id, test_result='Positive', ignore=False).earliest('adjusted_date').adjusted_date
        except DiagnosticTestHistory.DoesNotExist:
            tci_end = None
                    
        try:
            tci_begin = DiagnosticTestHistory.objects.filter(subject__id=subject_id, test_result='Negative', ignore=False).latest('adjusted_date').adjusted_date
        except DiagnosticTestHistory.DoesNotExist:
            tci_begin = None

        if tci_begin is None or tci_end is None:
            eddi = None
            tci_size = None
        else:
            eddi = tci_begin + timedelta(days=((tci_end - tci_begin).days / 2))
            tci_size = abs((tci_end - tci_begin).days)

        subject = Subject.objects.get(pk=subject_id)
        if subject.edsc_reported and eddi:
            edsc_days_diff = timedelta(days=(eddi - subject.edsc_reported).days).days
                
        subject_to_update = Subject.objects.get(pk=subject_id)
        new_eddi = SubjectEDDI.objects.create(tci_begin=tci_begin,
                                              tci_end=tci_end,
                                              tci_size=tci_size,
                                              edsc_days_difference=edsc_days_diff,
                                              eddi=eddi)

        subject_to_update.subject_eddi = new_eddi
        subject_to_update.save()
