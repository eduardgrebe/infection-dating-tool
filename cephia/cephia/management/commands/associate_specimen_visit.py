from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from cephia.models import Specimen, Visit
from datetime import timedelta
from django.db.models import Min
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Associate specimen with visits'

    def handle(self, *args, **options):
        num_associations = 0

        for specimen in Specimen.objects.filter(visit__isnull=True, subject__isnull=False, reported_draw_date__isnull=False):
            try:
                visit = Visit.objects.get(subject=specimen.subject, visit_date=specimen.reported_draw_date)
                specimen.visit_linkage = 'exact'
            except Visit.DoesNotExist:
                from_date = specimen.reported_draw_date - timedelta(days=14)
                to_date = specimen.reported_draw_date + timedelta(days=14)
                possible_visits = Visit.objects.filter(subject=specimen.subject,
                                                       visit_date__gte=from_date,
                                                       visit_date__lte=to_date)

                if possible_visits.count() > 1:
                    day_differences = [ {specimen.reported_draw_date - visit.visit_date: visit} for visit in possible_visits ]
                    visit = min(day_differences).values()[0]
                    specimen.visit_linkage = 'provisional'
                elif possible_visits.count() == 0:
                    continue
                else:
                    visit = possible_visits[0]
                    specimen.visit_linkage = 'provisional'

            specimen.visit = visit
            specimen.source_study = visit.source_study
            specimen.save()

            num_associations = num_associations + 1

        logger.info('Successfully associated "%s" visits with subjects' % num_associations)
