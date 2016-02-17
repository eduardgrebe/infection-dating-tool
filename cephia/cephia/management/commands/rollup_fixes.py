from django.core.management.base import BaseCommand, CommandError
from cephia.file_handlers.file_handler import FileHandler
from datetime import datetime, date
from cephia.file_handlers.handler_imports import *
from cephia.models import (Subject, SubjectRow, FileInfo,
                           TransferInRow, Specimen, Location, SpecimenType)
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fix rereported roll up specimens'

    def validate_row(self, handler, row):
        default_less_date = datetime.now().date() - relativedelta(years=75)
        default_more_date = datetime.now().date() + relativedelta(years=75)
        
        error_msg = ''
        handler.register_dates(row.model_to_dict())

        if not row.volume:
            error_msg += 'volume is required.\n'

        if not row.volume_units:
            error_msg += 'volume_units is required.\n'
                
        if not row.number_of_containers:
            error_msg += 'Number of containers is required.\n'
                
        if not handler.registered_dates.get('drawdate', default_less_date) < handler.registered_dates.get('transfer_date', default_more_date):
            error_msg += 'draw_date must be before transfer_date. '

        if not handler.registered_dates.get('transfer_date', default_less_date) <= datetime.now().date():
            error_msg += 'transfer_date must be before today.\n'

        try:
            SpecimenType.objects.get(spec_type=row.specimen_type)
        except SpecimenType.DoesNotExist:
            error_msg += "Reported specimen_type not recognised.\n"

        if not row.subject_label:
            error_msg += "subject_label cannot be blank.\n"

        if row.specimen_type in ['1','3','4.1','4.2','6', '8']:
            if row.volume_units != 'microlitres':
                error_msg += 'volume_units must be "microlitres" for this specimen_type.\n'
            if float(row.volume or 0) < 90:
                error_msg += 'volume must be greater than 90 for this specimen type.\n'

        if row.specimen_type == '2':
            if row.volume_units not in ['cards','microlitres']:
                error_msg += 'volume_units must be either "cards" or "microlitres" for this specimen_type.\n'
            if row.volume_units == 'cards' and float(row.volume or 0) > 20:
                error_msg += 'volume must be less than 20 for this specimen_type and volume unit.\n'
            if row.volume_units == 'microlitres' and float(row.volume or 0) < 20:
                error_msg += 'volume must be greater than 20 for this specimen type and volume unit.\n'

        if row.specimen_type in ['5.1','5.2']:
            if row.volume_units != 'grams':
                error_msg += 'volume_units must be "grams" for this specimen_type.\n'
            if float(row.volume or 0) > 100:
                error_msg += 'volume must be less than 100 for this specimen_type.\n'

        if row.specimen_type == '7':
            if row.volume_units not in ['m cells', 'microlitres']:
                error_msg += 'volume_units must be either "m cells" or "microlitres" for this specimen_type.\n'
            if row.volume_units == 'm cells' and float(row.volume or 0) > 20:
                error_msg += 'volume must be less than 20 for this specimen_type and volume unit.\n'
            if row.volume_units == 'microlitres' and float(row.volume or 0) < 90:
                error_msg += 'volume must be greater than 90 for this specimen_type and volume unit.\n'

        if row.specimen_type in ['10.1','10.2']:
            if row.volume_units != 'swabs':
                error_msg += 'volume_units must be "swabs" for this specimen_type.\n'
            if float(row.volume or 0) > 10:
                error_msg += 'volume must be less than or equal to 10 for this specimen_type.\n'

        return error_msg

    def handle(self, *args, **options):
        upload_file = FileInfo.objects.get(pk=78)
        handler = upload_file.get_handler()
        #handler.parse()
        uploaded_rows = TransferInRow.objects.filter(fileinfo=upload_file)

        for row in uploaded_rows:
            try:
                handler.register_dates(row.model_to_dict())
                error_msg = self.validate_row(handler, row)
                if error_msg:
                    raise Exception(error_msg)
            
                try:
                    subject = Subject.objects.get(subject_label=row.subject_label)
                except Subject.DoesNotExist:
                    subject = None
                    pass
            
                spec = Specimen.objects.filter(specimen_label=row.specimen_label,
                                               specimen_type__spec_type=row.specimen_type)

                if spec.count() > 1:
                    msg = "More than 1 found (%s)" % spec.specimen_label
                    raise Exception(msg)
                elif spec.count() > 0:
                    specimen = spec[0]
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
                else:
                    row.state = 'error'
                    row.error_message = 'to be reuploaded - not included rollup fix script'
                    row.save()
            except Exception, e:
                row.state = 'error'
                row.error_message = e.message
                row.save()

        upload_file.state = 'processed'
        upload_file.message = 'rollup fix'
        upload_file.save()
                    
        logger.info('Rollup fix - Success!')
