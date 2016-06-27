from django.core.management.base import BaseCommand, CommandError
from cephia.models import Visit, Subject
from django.db.models import Q, F
from django.db import transaction
import logging

logger = logging.getLogger(__name__)
import traceback

class Command(BaseCommand):
    help = 'Calculate visit details for each visit'

    def handle(self, *args, **options):
        with transaction.atomic():
            for visit in Visit.objects.select_related('subject', 'visitdetail', 'subject__subject_eddi'):
                with transaction.atomic():
                    try:
                        visit.update_visit_detail()
                    except Exception, e:
                        logger.error('Error with creating detail for visit: %s' % visit.pk)
                        traceback.print_exc()
                        continue
