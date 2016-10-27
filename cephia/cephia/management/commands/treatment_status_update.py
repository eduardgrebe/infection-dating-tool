from django.core.management.base import BaseCommand, CommandError
from cephia.models import Visit, Subject
from django.db.models import Q, F
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update all subjects to have a treatment status'

    def handle(self, *args, **options):
        with transaction.atomic():

            all_visits = Visit.objects.all()

            treatment_naive = all_visits.filter(
                Q(subject__isnull=False,
                  subject__art_initiation_date__isnull=False,
                  visit_date__lte=F('subject__art_initiation_date')) |
                Q(subject__art_initiation_date__isnull=True))

            treatment_naive.update(treatment_naive=True, on_treatment=False)

            on_treatment = all_visits.filter(
                Q(subject__isnull=False,
                  subject__art_initiation_date__isnull=False,
                  visit_date__gt=F('subject__art_initiation_date')))
            
            on_treatment = on_treatment.filter(
                Q(visit_date__lt=F('subject__art_interruption_date')) |
                Q(visit_date__gt=F('subject__art_resumption_date')) |
                Q(subject__art_interruption_date__isnull=True)
            )
            
            on_treatment.update(on_treatment=True, treatment_naive=False)

            on_interruption  = all_visits.filter(
                Q(subject__isnull=False,
                  subject__art_initiation_date__isnull=False,
                  visit_date__gt=F('subject__art_interruption_date'))
            )
            on_interruption = on_interruption.filter(
                Q(visit_date__lt=F('subject__art_resumption_date')) |
                Q(subject__art_resumption_date__isnull=True)
            )
            on_interruption.update(on_treatment=False, treatment_naive=False)

            #FOR FIRST TREATMENT CALCULATION
            on_treatment = all_visits.filter(on_treatment=True)
            not_on_treatment = all_visits.filter(on_treatment=False)
            not_on_treatment.update(first_treatment=None)

            on_first_treatment = on_treatment.filter(
                Q(subject__art_interruption_date__isnull=True) |
                Q(visit_date__lt=F('subject__art_interruption_date')))
            not_first_treatment = on_treatment.exclude(pk__in=[ visit.id for visit in on_first_treatment ])

            on_first_treatment.update(first_treatment=True)
            not_first_treatment.update(first_treatment=False)

