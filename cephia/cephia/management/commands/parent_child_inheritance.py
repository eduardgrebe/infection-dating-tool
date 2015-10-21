from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from cephia.models import Specimen, Subject
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Children specimen to inherit all parent specimens properties'

    def handle(self, *args, **options):
        num_inherited = 0

        for specimen in Specimen.objects.filter(subject__isnull=True, visit__isnull=True, parent__isnull=False):
            try:
                parent_specimen = Specimen.objects.get(specimen_label=aliquot_row.parent_label, parent_label=None)

                specimen.update(specimen_type=parent_specimen.specimen_type,
                                reported_draw_date=parent_specimen.reported_draw_date,
                                transfer_in_date=parent_specimen.transfer_in_date,
                                parent=parent_specimen,
                                visit=parent_specimen.visit,
                                subject=parent_specimen.subject,
                                source_study=parent_specimen.source_study)

            num_inherited = num_inherited + 1

        logger.info('Successfully associated "%s" visits with subjects' % num_associations)
