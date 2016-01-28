from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from cephia.models import Subject, SubjectEDDI
from diagnostics.models import DiagnosticTestHistory
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update EDDI dates on subjects table'

    def handle(self, *args, **options):
        subject_ids = DiagnosticTestHistory.objects.values_list('subject_id', flat=True).distinct()
        for subject_id in subject_ids:
            try:
                tci_end = DiagnosticTestHistory.objects.filter(subject__id=subject_id, test_result='Positive').earliest('adjusted_date').adjusted_date
            except DiagnosticTestHistory.DoesNotExist:
                tci_end = None
                    
            try:
                tci_begin = DiagnosticTestHistory.objects.filter(subject__id=subject_id, test_result='Negative').latest('adjusted_date').adjusted_date
            except DiagnosticTestHistory.DoesNotExist:
                tci_begin = None

            if tci_begin is None or tci_end is None:
                eddi = None
            else:
                eddi = tci_begin + timedelta(days=((tci_end - tci_begin).days / 2))
                tci_size = abs((tci_end - tci_begin).days)

            subject_eddi = SubjectEDDI.objects.create(tci_begin=tci_begin,
                                                      tci_end=tci_end,
                                                      tci_size=tci_size,
                                                      eddi=eddi)

            subject_to_update = Subject.objects.get(pk=subject_id)
            subject_to_update.subject_eddi = subject_eddi
            subject_to_update.save()
