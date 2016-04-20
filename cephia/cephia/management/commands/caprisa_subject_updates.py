from django.core.management.base import BaseCommand, CommandError
import datetime
from cephia.models import Subject
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update information on certain caprisa subjects'

    def handle(self, *args, **options):
        subject_file = open('cephia/management/commands/20160420_subjectsfixes.csv', 'r')
        headers = subject_file.readline().strip().split(',')
        for row in subject_file.readlines():
            try:
                line = row.strip().split(',')
                subject_row = dict(zip(headers, line))
                subject = Subject.objects.get(subject_label=subject_row['subject_label'])
                if subject_row['update_first_positive_date']:
                    subject.first_positive_date = datetime.datetime.strptime(subject_row['update_first_positive_date'], "%Y-%m-%d").date()
                if subject_row['update_last_negative_date']:
                    subject.last_negative_date = datetime.datetime.strptime(subject_row['update_last_negative_date'], "%Y-%m-%d").date()
                if subject_row['update_art_initiation_date']:
                    subject.art_initiation_date = datetime.datetime.strptime(subject_row['update_art_initiation_date'], "%Y-%m-%d").date()
                subject.save()
            except Exception, e:
                logger.exception(e)
                subject_file.close()
        subject_file.close()
