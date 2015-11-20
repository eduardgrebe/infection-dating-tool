from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from cephia.models import Specimen, Subject
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Children specimen to inherit all parent specimens properties'

    def handle(self, *args, **options):
        num_inherited = 0

        for specimen in Specimen.objects.filter(Q(subject__isnull=True) | Q(visit__isnull=True), parent__isnull=False):
            try:
                parent_specimen = specimen.parent
                
                specimen.specimen_type = parent_specimen.specimen_type
                specimen.reported_draw_date=parent_specimen.reported_draw_date
                specimen.transfer_in_date=parent_specimen.transfer_in_date
                specimen.parent=parent_specimen
                specimen.visit=parent_specimen.visit
                specimen.subject=parent_specimen.subject
                specimen.source_study=parent_specimen.source_study

                specimen.save()

            except Specimen.DoesNotExist:
                continue

            num_inherited += 1

        logger.info('Successfully associated "%s" visits with subjects' % num_inherited)
