from django.core.management.base import BaseCommand, CommandError
from cephia.models import Visit, Subject
from django.db.models import Q, F
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update all subjects to have a treatment status'

    def handle(self, *args, **options):
        treatment_naive = Visit.objects.filter(Q(subject__isnull=False,
                                                 subject__art_initiation_date__isnull=False,
                                                 visit_date__lt=F('subject__art_initiation_date')) |
                                               Q(subject__art_initiation_date__isnull=True))

        on_treatment = Visit.objects.filter(Q(subject__isnull=False,
                                              subject__art_initiation_date__isnull=False,
                                              visit_date__gt=F('subject__art_initiation_date')))
        on_treatment = on_treatment.filter(Q(visit_date__lt=F('subject__art_interruption_date')) |
                                            Q(visit_date__gt=F('subject__art_resumption_date')) |
                                            Q(subject__art_interruption_date__isnull=True))

        treatment_naive.update(treatment_naive=True, on_treatment=False)
        on_treatment.update(on_treatment=True, treatment_naive=False)
