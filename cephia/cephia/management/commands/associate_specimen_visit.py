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

        for specimen in Specimen.objects.filter(visit=None, subject__isnull=False):
            try:
                visit = Visit.objects.get(subject=specimen.subject, visit_date=specimen.reported_draw_date)

            except Visit.DoesNotExist:
                from_date = specimen.reported_draw_date - timedelta(days=14)
                to_date = specimen.reported_draw_date + timedelta(days=14)
                possible_visits = Visit.objects.filter(subject=specimen.subject,
                                                       visit_date__gte=from_date,
                                                       visit_date__lte=to_date)

                if possible_visits.count() > 1:
                    import pdb; pdb.set_trace()
                    visit = possible_visits.aggregate(Min(visit_date))
                elif possible_visits.count() == 0:
                    continue
                else:
                    visit = possible_visits[0]

            specimen.visit = visit
            specimen.source_study = visit.source_study
            specimen.visit_linkage = 'provisional'
            specimen.save()

            num_associations = num_associations + 1

        logger.info('Successfully associated "%s" visits with subjects' % num_associations)
