from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from cephia.models import Specimen, Subject
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Associate specimen with subject'

    def handle(self, *args, **options):
        num_associations = 0

        for specimen in Specimen.objects.filter(subject=None):
            try:
                subject = Subject.objects.get(subject_label=specimen.subject_label)
                specimen.subject = subject
                specimen.save()
            except Subject.DoesNotExist:
                continue

            num_associations = num_associations + 1

        logger.info('Successfully associated "%s" visits with subjects' % num_associations)
