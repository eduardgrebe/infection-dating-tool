from django.core.management.base import BaseCommand, CommandError
import datetime
from assay.models import AssayRun
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Recalculate the visit id for and assay'
    args = '<assay_run_id>'

    def handle(self, *args, **kwargs):
        try:
            args[0]
        except IndexError:
            raise CommandError("Error: Assay run id required")
        AssayRun.objects.get(pk=args[0]).check_replicate_counts()
