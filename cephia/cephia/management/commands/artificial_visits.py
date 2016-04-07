from django.core.management.base import BaseCommand, CommandError
import datetime
from cephia.models import Visit, Panel, PanelMemberships
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Artificial visits to be marked with boolean to identify them'

    def handle(self, *args, **options):
        the_file = open('artificial_visits.csv', 'r')
        error_file = open('artificial_visit_errors.csv', 'w')
        for row in the_file.readlines():
            if 'subject_label' not in row:
                try:
                    line = row.split(',')
                    visit = Visit.objects.get(subject_label=line[0],
                                              visit_date=datetime.datetime.strptime(line[1].strip(), "%m/%d/%Y").date())
                    visit.artificial = True
                    visit.save()
                except Exception, e:
                    error_file.write(row)
        error_file.close()
        the_file.close()
