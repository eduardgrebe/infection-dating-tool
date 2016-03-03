from django.core.management.base import BaseCommand, CommandError
from cephia.models import Specimen, AliquotRow, HistoricalAliquotRow
from django.db.models import F
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Specimen with the same parent and specimen label to be used as volume updates and deleted'

    def handle(self, *args, **options):
        specimens = Specimen.objects.filter(specimen_label=F('parent_label'))
        for specimen in specimens:
            root_specimen = Specimen.objects.get(specimen_label=specimen.specimen_label,
                                                 parent_label=None,
                                                 specimen_type=specimen.specimen_type)
            root_specimen.volume = specimen.volume
            root_specimen.save()
            AliquotRow.objects.filter(specimen=specimen).delete()
            HistoricalAliquotRow.objects.filter(specimen=specimen).delete()
            specimen.delete()
