from django.core.management.base import BaseCommand, CommandError
from cephia.file_handlers.file_handler import FileHandler
from datetime import datetime, date
from cephia.file_handlers.handler_imports import *
from cephia.models import Subject, SubjectRow, FileInfo
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Add edsc reported below and above the line for existing rows'

    def handle(self, *args, **options):
        upload_file = FileInfo.objects.get(pk=8)
        handler = FileHandler(upload_file)
        
        for row_num in range(handler.num_rows):
            if row_num >= 1:
                row_dict = dict(zip(handler.header, handler.file_rows[row_num]))
                if not row_dict:
                    continue

                if row_dict['edsc_reported_yyyy']:
                    try:
                        subject_row = SubjectRow.objects.get(subject_label=row_dict['subject_label'],
                                                             state='processed')
                    except SubjectRow.DoesNotExist:
                        continue

                    subject_row.edsc_reported_yyyy = row_dict['edsc_reported_yyyy']
                    subject_row.edsc_reported_mm = row_dict['edsc_reported_mm']
                    subject_row.edsc_reported_dd = row_dict['edsc_reported_dd']
                    subject_row.save()
                    edsc_reported = date(year=int(row_dict['edsc_reported_yyyy']),
                                         month=int(row_dict['edsc_reported_mm']),
                                         day=int(row_dict['edsc_reported_dd']))
                    subject = subject_row.subject
                    subject.edsc_reported = edsc_reported or None
                    subject.save()

        upload_file.state = 'processed'
        upload_file.message = 'edsc fix'
        upload_file.save()
        logger.info('EDSC fix - Success!')



