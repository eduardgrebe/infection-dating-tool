from file_handler import FileHandler
from handler_imports import *
import logging

logger = logging.getLogger(__name__)


class AliquotFileHandler(FileHandler):

    def __init__(self, aliquot_file):
        super(AliquotFileHandler, self).__init__()
        self.aliquot_file = aliquot_file
        self.excel_aliquot_file = ExcelHelper(f=aliquot_file.data_file.url)
        self.aliquot_row = None

        self.registered_columns = ['parent_label',
                                   'aliquot_label',
                                   'aliquoting_date_yyyy',
                                   'aliquoting_date_mm',
                                   'aliquoting_date_dd',
                                   'specimen_type',
                                   'volume',
                                   'volume_units',
                                   'reason']

        self.existing_columns = self.excel_aliquot_file.read_header()

    def parse(self):
        from cephia.models import AliquotRow

        header = self.excel_aliquot_file.read_header()
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.excel_aliquot_file.nrows):
            try:
                if row_num >= 1:
                    row = self.excel_aliquot_file.read_row(row_num)
                    row_dict = dict(zip(header, row))
                    
                    aliquot_row = AliquotRow.objects.create(parent_label=row_dict['parent_label'],
                                                            aliquot_label=row_dict['aliquot_label'],
                                                            volume=row_dict['volume'],
                                                            volume_units=row_dict['volume_units'],
                                                            aliquoting_date_yyyy=row_dict['aliquoting_date_yyyy'],
                                                            aliquoting_date_mm=row_dict['aliquoting_date_mm'],
                                                            aliquoting_date_dd=row_dict['aliquoting_date_dd'],
                                                            aliquot_reason=row_dict['reason'],
                                                            fileinfo=self.aliquot_file,
                                                            state='pending')


                    rows_inserted += 1

            except Exception, e:
                logger.exception(e)
                self.aliquot_file.message = "row " + str(row_num) + ": " + e.message
                self.aliquot_file.save()
                return 0, 1

        return rows_inserted, rows_failed
    
    def validate(self):
        from cephia.models import AliquotRow
        
        default_less_date = datetime.now().date() - relativedelta(years=75)
        default_more_date = datetime.now().date() + relativedelta(years=75)
        rows_validated = 0
        rows_failed = 0
        
        for aliquot_row in AliquotRow.objects.filter(fileinfo=self.aliquot_file, state='pending'):
            try:
                #self.register_dates(aliquot_row.model_to_dict())

                # if not self.registered_dates.get('drawdate', default_less_date) < self.registered_dates.get('transfer_date', default_more_date):
                #     raise Exception('draw_date must be smaller than transfer_date')

                try:
                    Specimen.objects.get(specimen_label=aliquot_row.parent_label, parent_label=None)
                except Specimen.DoesNotExist:
                    raise Exception("Parent specimen does not exist")

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

        for aliquot_row in AliquotRow.objects.filter(fileinfo=self.aliquot_file, state='validated'):

            try:
                with transaction.atomic():
                    self.register_dates(aliquot_row.model_to_dict())

                    parent_specimen = Specimen.objects.get(specimen_label=aliquot_row.parent_label, parent_label=None)
                    
                    if aliquot_row.parent_label == aliquot_row.aliquot_label:
                        parent_specimen.volume = aliquot_row.volume
                        parent_specimen.modified_date = self.registered_dates('aliquot_date', None)
                        parent_specimen.reason = aliquot_row.aliquot_reason
                        parent_specimen.save()
                    else:
                        parent_specimen.modified_date = self.registered_dates('aliquot_date', None)
                        parent_specimen.save()

                        Specimen.objects.create(specimen_label=aliquot_row.aliquot_label,
                                                parent_label=aliquot_row.parent_label,
                                                volume=aliquot_row.volume,
                                                volume_units=aliquot_row.volume_units,
                                                specimen_type=parent_specimen.specimen_type,
                                                reported_draw_date=parent_specimen.reported_draw_date,
                                                source_study=parent_specimen.source_study,
                                                created_date=self.registered_dates('aliquot_date', None),
                                                aliquoting_reason=aliquot_row.aliquot_reason)
                        
                    aliquot_row.state = 'processed'
                    aliquot_row.error_message = ''
                    aliquot_row.date_processed = timezone.now()
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
