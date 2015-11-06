from django.core.management.base import BaseCommand, CommandError
from cephia.file_handlers.file_handler import FileHandler
from datetime import datetime, date
from cephia.file_handlers.handler_imports import *
from cephia.models import Visit, VisitRow, FileInfo
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Add scope_ec below and above the line for existing rows'

    def handle(self, *args, **options):
        upload_file = FileInfo.objects.get(pk=9)
        handler = FileHandler(upload_file)

        for row_num in range(handler.num_rows):
            if row_num >= 1:
                row_dict = dict(zip(handler.header, handler.file_rows[row_num]))
                if not row_dict:
                    continue

                if row_dict['scopevisit_ec']:
                    try:
                        visit_row = VisitRow.objects.get(subject_label=row_dict['subject_label'],
                                                         visitdate_yyyy=row_dict['visitdate_yyyy'],
                                                         visitdate_mm=row_dict['visitdate_mm'],
                                                         visitdate_dd=row_dict['visitdate_dd'],
                                                         state='processed')
                    except VisitRow.DoesNotExist:
                        continue

                    visit_row.scopevisit_ec = row_dict['scopevisit_ec']
                    visit_row.save()
                    visit = visit_row.visit
                    visit.scopevisit_ec = handler.get_bool(row_dict['scopevisit_ec']) or False
                    visit.save()

        upload_file.state = 'processed'
        upload_file.message = 'scope ec fix'
        upload_file.save()
        logger.info('ScopeEC fix - Success!')



