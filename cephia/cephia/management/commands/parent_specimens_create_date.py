from django.core.management.base import BaseCommand, CommandError
from cephia.models import Specimen
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Make parent specimen create dates equal to transfer in dates'

    def handle(self, *args, **options):
        with transaction.atomic():
            parent_specimens = Specimen.objects.filter(parent_label__isnull=True)
            for specimen in parent_specimens:
                specimen.created_date = specimen.transfer_in_date
                specimen.save()
