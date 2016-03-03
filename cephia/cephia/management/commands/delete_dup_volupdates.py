from django.core.management.base import BaseCommand, CommandError
from cephia.models import Specimen, AliquotRow, HistoricalAliquotRow
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Remove duplicate volume update records from aliquot files'

    def handle(self, *args, **options):
        aliquots_file = open('volupdate_duplicate_records.csv')
        for line in aliquots_file.readlines():
            current_row = line.split(',')
            if not 'specimen_label' in current_row:
                specimen = Specimen.objects.filter(specimen_label=current_row[0],
                                                   parent_label=current_row[1],
                                                   specimen_type__id=current_row[2]).first()
                AliquotRow.objects.filter(specimen=specimen).delete()
                HistoricalAliquotRow.objects.filter(specimen=specimen).delete()
                specimen.delete()

        spec = Specimen.objects.filter(specimen_label='00C305004V21.1',
                                       parent_label='00C305004V21.1',
                                       specimen_type__id=10).first()
        AliquotRow.objects.filter(specimen=spec).delete()
        HistoricalAliquotRow.objects.filter(specimen=spec).delete()
        spec.delete()
