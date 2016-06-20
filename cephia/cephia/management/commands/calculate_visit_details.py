from django.core.management.base import BaseCommand, CommandError
from cephia.models import Visit, Subject
from django.db.models import Q, F
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Calculate visit details for each visit'

    def handle(self, *args, **options):
        with transaction.atomic():
            for visit in Visit.objects.select_related('subject'):
                visit.update_visit_detail()
