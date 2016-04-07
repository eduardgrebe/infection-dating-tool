from django.core.management.base import BaseCommand, CommandError
import datetime
from cephia.models import Visit, Panel, PanelMemberships
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Add visits from file to HRBS panel membership'

    def handle(self, *args, **options):
        the_file = open('in_hrbs_panels.csv', 'r')
        error_file = open('hrbs_errors.csv', 'w')
        hrbs_panel, created = Panel.objects.get_or_create(name='HRBS')
        for row in the_file.readlines():
            if 'SubjectLabel' not in row:
                try:
                    line = row.split(',')
                    visit = Visit.objects.get(subject_label=line[0],
                                              visit_date=datetime.datetime.strptime(line[1].strip(), "%Y-%m-%d").date())
                    PanelMemberships.objects.create(panel=hrbs_panel, visit=visit)
                except Exception, e:
                    error_file.write(row)
        error_file.close()
        the_file.close()
