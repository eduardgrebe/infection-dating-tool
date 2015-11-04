from django.core.management.base import BaseCommand, CommandError
from cephia.file_handlers.file_handler import FileHandler
from datetime import datetime, date
from cephia.file_handlers.handler_imports import *
from cephia.models import Subject, SubjectRow
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Add edsc reported below and above the line for exiting rows'

    def handle(self, *args, **options):
        import pdb; pdb.set_trace()
        filename = 'scope_ec_fix.csv'
        upload_file = FileInfo.objects.get(filename=filename)
        handler = FileHandler(upload_file)
        
        for row_num in range(handler.num_rows):
            if row_num >= 1:
                row_dict = dict(zip(handler.header, hanlder.file_rows[row_num]))
                if not row_dict:
                    continue

            if row_dict['scopevisit_ec']:
                visit_row = SubjectRow.objects.get(subject_label=row_dict['subject_label'],
                                                   visitdate_yyyy=row_dict['visitdate_yyyy'],
                                                   visitdate_mm=row_dict['visitdate_mm'],
                                                   visitdate_dd=row_dict['visitdate_dd'])
                visit_row.scopevisit_ec = row_dict['scopevisit_ec']
                visit_row.save()
                visit = visit_row.visit
                visit.scopevisit_ec = handler.get_bool(row_dict['scopevisit_ec']) or False
                visit_row.save()

        logger.info('ScopeEC fix - Success!')



