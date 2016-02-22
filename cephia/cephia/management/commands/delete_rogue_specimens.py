from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from cephia.models import TransferInRow, Specimen
from diagnostics.models import DiagnosticTestHistory
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Delete rogue specimens accidently reported'
    args = '<type>'

    def handle(self, *args, **options):
        spec_file = open('BSRI_transferin_delete20160217_revised.csv')
        for line in spec_file.readlines():
            row_id = line.split(',')[0].rstrip()
            try:
                spec_row = TransferInRow.objects.get(pk=row_id)
                if spec_row.specimen:
                    spec_row.specimen.delete()
                spec_row.delete()
            except TransferInRow.DoesNotExist:
                continue

