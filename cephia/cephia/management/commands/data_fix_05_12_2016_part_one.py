from django.core.management.base import BaseCommand, CommandError
from cephia.models import Visit, Subject
from datetime import datetime
from django.db.models import Q, F
from django.db import transaction
import logging
import traceback

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update vl_reported for one visit and cohort entry dates for selected subjects. To be done before visits error file is uploaded.'

    def handle(self, *args, **options):
        self.fix_visit_details()

    def fix_visit_details(self):
        visit_lines = [['22747', 'vl_reported', '19110'],
                 ['0917600092', 'cohort_entry_date', '2015-3-26'],
                 ['0917600185', 'cohort_entry_date', '2015-3-12'],
                 ['0917600235', 'cohort_entry_date', '2015-3-27'],
                 ['0917600248', 'cohort_entry_date', '2015-3-31'],
                 ['0918000026', 'cohort_entry_date', '2014-11-6'],
                 ['0918000033', 'cohort_entry_date', '2014-5-22'],
                 ['0918000057', 'cohort_entry_date', '2013-7-3'],
                 ['0918000064', 'cohort_entry_date', '2015-4-8'],
                 ['0918000076', 'cohort_entry_date', '2015-5-18'],
                 ['0918000083', 'cohort_entry_date', '2014-1-28'],
                 ['0918000104', 'cohort_entry_date', '2013-12-13'],
                 ['0918000117', 'cohort_entry_date', '2015-1-16'],
                 ['0918000121', 'cohort_entry_date', '2014-1-29'],
                 ['0918000131', 'cohort_entry_date', '2015-2-4'],
                 ['0918000154', 'cohort_entry_date', '2013-3-20'],
                 ['0918000184', 'cohort_entry_date', '2015-6-3'],
                 ['0918000226', 'cohort_entry_date', '2015-2-11'],
                 ['0918000277', 'cohort_entry_date', '2015-5-6'],
                 ['0918000313', 'cohort_entry_date', '2015-5-21']
        ]

        for i in visit_lines:
            object_id = i[0]
            field = i[1]
            value = i[2]

            if field == 'vl_reported':
                value = int(value)
                visit = Visit.objects.get(pk=object_id)
                visit.vl_reported = value
                visit.save()
            elif field == 'cohort_entry_date':
                value = datetime.strptime(value, '%Y-%m-%d')
                subject = Subject.objects.get(subject_label=object_id)
                subject.cohort_entry_date = value.date()
                subject.save()