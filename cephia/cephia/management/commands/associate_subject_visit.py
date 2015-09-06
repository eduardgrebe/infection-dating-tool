from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from cephia.models import Subject, Visit
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Associate subjects with visits'

    def handle(self, *args, **options):
        num_associations = 0

        for visit in Visit.objects.filter(subject__isnull=True):
            try:
                subject = Subject.objects.get(subject_label=visit.subject_label)
                visit.subject = subject
                visit.save()
            except Subject.DoesNotExist:
                continue

            num_associations = num_associations + 1

        logger.info('Successfully associated "%s" visits with subjects' % num_associations)
