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
            #what if only pos or neg exist?
            tci_begin = DiagnosticTestHistory.objects.filter(subject__id=subject_id, test_result='Negative').latest('adjusted_date').adjusted_date
            tci_end = DiagnosticTestHistory.objects.filter(subject__id=subject_id, test_result='Positive').earliest('adjusted_date').adjusted_date
            eddi = tci_begin + timedelta(days=((tci_begin - tci_end).days / 2))
                
            SubjectEDDI.objects.create(tci_begin=tci_begin,
                                       tci_end=tci_end,
                                       eddi=eddi)
