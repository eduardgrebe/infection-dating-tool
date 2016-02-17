from django.core.management.base import BaseCommand, CommandError
from cephia.file_handlers.file_handler import FileHandler
from datetime import datetime, date
from cephia.file_handlers.handler_imports import *
from cephia.models import (Subject, SubjectRow, FileInfo,
                           TransferInRow, Specimen, Location)
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fix rereported roll up specimens'

    def handle(self, *args, **options):
        upload_file = FileInfo.objects.get(pk=73)
        handler = upload_file.get_handler()
        uploaded_rows = TransferInRow.objects.filter(fileinfo=upload_file)

        for row in uploaded_rows:
            spec = Specimen.objects.filter(specimen_label=row.specimen_label,
                                           specimen_type__spec_type=row.specimen_type)
            if spec.count() > 1:
                msg = "More than 1 found (%s)" % spec.specimen_label
                raise Exception(msg)
            elif spec.count() > 0:
                specimen = spec[0]
                handler.register_dates(row.model_to_dict())
                try:
                    subject = Subject.objects.get(subject_label=row.subject_label)
                except Subject.DoesNotExist:
                    subject = None
                    pass
                
                specimen.subject_label = row.subject_label
                specimen.reported_draw_date = handler.registered_dates.get('drawdate', None)
                specimen.transfer_in_date = handler.registered_dates.get('transfer_date', None)
                specimen.transfer_reason = row.transfer_reason
                specimen.subject = subject
                specimen.number_of_containers = (row.number_of_containers or None)
                specimen.initial_claimed_volume = (float(row.volume) * float(row.number_of_containers))
                specimen.volume_units = row.volume_units
                specimen.source_study = None
                specimen.location = Location.objects.get(name=row.location)
                specimen.is_available = True
                specimen.save()

                row.state = 'processed'
                row.specimen = specimen
                row.save()

        upload_file.state = 'processed'
        upload_file.message = 'rollup fix'
        upload_file.save()
                    
        logger.info('Rollup fix - Success!')
