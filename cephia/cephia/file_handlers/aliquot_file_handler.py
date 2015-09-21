from file_handler import FileHandler
from handler_imports import *
import logging

logger = logging.getLogger(__name__)


class AliquotFileHandler(FileHandler):

    def __init__(self, upload_file):
        super(AliquotFileHandler, self).__init__(upload_file)

        self.registered_columns = ['parent_label',
                                   'aliquot_label',
                                   'aliquoting_date_yyyy',
                                   'aliquoting_date_mm',
                                   'aliquoting_date_dd',
                                   'specimen_type',
                                   'volume',
                                   'volume_units',
                                   'reason']

    def parse(self):
        from cephia.models import AliquotRow

        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    
                    if row_dict.get('id', None):
                        aliquot_row = AliquotRow.objects.get(pk=row_dict['id'])
                    else:
                        aliquot_row = AliquotRow.objects.create(parent_label=row_dict['parent_label'],
                                                                aliquot_label=row_dict['aliquot_label'],
                                                                fileinfo=self.upload_file)
                    
                    aliquot_row.volume=row_dict['volume']
                    aliquot_row.volume_units=row_dict['volume_units']
                    aliquot_row.aliquoting_date_yyyy=row_dict['aliquoting_date_yyyy']
                    aliquot_row.aliquoting_date_mm=row_dict['aliquoting_date_mm']
                    aliquot_row.aliquoting_date_dd=row_dict['aliquoting_date_dd']
                    aliquot_row.aliquot_reason=row_dict['reason']
                    aliquot_row.state='pending'
                    aliquot_row.error_message = ''
                    aliquot_row.fileinfo=self.upload_file
                    aliquot_row.save()

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1

        return rows_inserted, rows_failed
    
    def validate(self):
        from cephia.models import AliquotRow, Specimen
        
        default_less_date = datetime.now().date() - relativedelta(years=75)
        default_more_date = datetime.now().date() + relativedelta(years=75)
        rows_validated = 0
        rows_failed = 0
        
        for aliquot_row in AliquotRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''
                self.register_dates(aliquot_row.model_to_dict())
                
                try:
                    specimen = Specimen.objects.get(specimen_label=aliquot_row.parent_label, parent_label=None)
                except Specimen.DoesNotExist:
                    erorr_msg += "Parent specimen does not exist.\n"

                if not self.registered_dates.get('aliquot_date', default_less_date) < (specimen.transfer_in_date or default_more_date):
                    error_msg += 'aliquot_date must be after transfer_in_date.\n'

                if error_msg:
                    raise Exception(error_msg)    

                aliquot_row.state = 'validated'
                aliquot_row.error_message = ''
                rows_validated += 1
                aliquot_row.save()
            except Exception, e:
                logger.exception(e)
                aliquot_row.state = 'error'
                aliquot_row.error_message = e.message
                rows_failed += 1
                aliquot_row.save()
                continue

        return rows_validated, rows_failed

    def process(self):
        from cephia.models import AliquotRow, Specimen
        
        rows_inserted = 0
        rows_failed = 0

        for aliquot_row in AliquotRow.objects.filter(fileinfo=self.upload_file, state='validated'):

            try:
                with transaction.atomic():
                    self.register_dates(aliquot_row.model_to_dict())

                    parent_specimen = Specimen.objects.get(specimen_label=aliquot_row.parent_label, parent_label=None)
                    
                    if aliquot_row.parent_label == aliquot_row.aliquot_label:
                        parent_specimen.volume = aliquot_row.volume
                        parent_specimen.modified_date = self.registered_dates.get('aliquot_date', None)
                        parent_specimen.reason = aliquot_row.aliquot_reason
                        parent_specimen.save()
                    else:
                        parent_specimen.modified_date = self.registered_dates.get('aliquot_date', None)
                        parent_specimen.save()

                        specimen = Specimen.objects.create(specimen_label=aliquot_row.aliquot_label,
                                                           parent_label=aliquot_row.parent_label,
                                                           volume=aliquot_row.volume,
                                                           volume_units=aliquot_row.volume_units,
                                                           specimen_type=parent_specimen.specimen_type,
                                                           reported_draw_date=parent_specimen.reported_draw_date,
                                                           transfer_in_date=parent_specimen.transfer_in_date,
                                                           source_study=parent_specimen.source_study,
                                                           created_date=self.registered_dates.get('aliquot_date', None),
                                                           aliquoting_reason=aliquot_row.aliquot_reason)
                        
                    aliquot_row.state = 'processed'
                    aliquot_row.error_message = ''
                    aliquot_row.date_processed = timezone.now()
                    aliquot_row.specimen = specimen
                    aliquot_row.save()

                    rows_inserted += 1

            except Exception, e:
                logger.exception(e)
                aliquot_row.state = 'error'
                aliquot_row.error_message = e.message
                aliquot_row.save()
                rows_failed += 1
                continue

        return rows_inserted, rows_failed
