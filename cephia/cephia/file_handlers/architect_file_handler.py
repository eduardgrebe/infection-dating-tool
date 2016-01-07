from file_handler import FileHandler
from handler_imports import *
import logging

logger = logging.getLogger(__name__)

class ArchitectFileHandler(FileHandler):
    upload_file = None
    
    def __init__(self, upload_file):
        super(ArchitectFileHandler, self).__init__(upload_file)

        self.registered_columns = ['Specimen ID',
                                   'Assay',
                                   'Sample Type',
                                   'Site',
                                   'Test Date',
                                   'Operator',
                                   'Assay Kit Lot ID',
                                   'Run/Plate ID',
                                   'Test Mode',
                                   'Well',
                                   'Intermediate 1',
                                   'Intermediate 2',
                                   'Intermediate 3',
                                   'Intermediate 4',
                                   'Intermediate 5',
                                   'Intermediate 6',
                                   'Final Result',
                                   'Panel Type']


    def parse(self):
        from assay.models import ArchitectResultRow
        
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    self.header = [ x.strip() for x in self.header ]
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    
                    architect_result_row = ArchitectResultRow.objects.create(specimen=row_dict['Specimen ID'],
                                                                 assay=row_dict['Assay'],
                                                                 sample_type=row_dict['Sample Type'],
                                                                 site=row_dict['Site'],
                                                                 test_date=row_dict['Test Date'],
                                                                 operator=row_dict['Operator'],
                                                                 assay_kit_lot_id=row_dict['Assay Kit Lot ID'],
                                                                 plate_id=row_dict['Run/Plate ID'],
                                                                 test_mode=row_dict['Test Mode'],
                                                                 well=row_dict['Well'],
                                                                 intermediate_1=row_dict['Intermediate 1'],
                                                                 intermediate_2=row_dict['Intermediate 2'],
                                                                 intermediate_3=row_dict['Intermediate 3'],
                                                                 intermediate_4=row_dict['Intermediate 4'],
                                                                 intermediate_5=row_dict['Intermediate 5'],
                                                                 intermediate_6=row_dict['Intermediate 6'],
                                                                 final_result=row_dict['Final Result'],
                                                                 panel_type=row_dict['Panel Type'],
                                                                 state='pending',
                                                                 fileinfo=self.upload_file)

                    rows_inserted += 1
            except Exception, e:
                import pdb; pdb.set_trace()
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1

        if rows_failed > 0:
            self.upload_file.state = 'row_error'
        else:
            self.upload_file.state = 'imported'
        fail_msg = 'Failed to import ' + str(rows_failed) + ' rows.'
        success_msg = 'Successfully imported ' + str(rows_inserted) + ' rows.'
        
        self.upload_file.message += fail_msg + '\n' + success_msg + '\n'
        self.upload_file.save()

    def validate(self):
        from cephia.models import Specimen
        from assay.models import ArchitectResultRow, ArchitectResult
        
        rows_validated = 0
        rows_failed = 0
        
        for architect_result_row in ArchitectResultRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''
                
                # try:
                #     Specimen.objects.get(pk=architect_result_row.specimen)
                # except Specimen.DoesNotExist:
                #     error_msg += "Specimen not recognised.\n"

                # try:
                #     Panel.objects.get(pk=architect_result_row.panel)
                # except Panel.DoesNotExist:
                #     error_msg += "Panel not recognised.\n"

                if error_msg:
                    raise Exception(error_msg)
                
                architect_result_row.state = 'validated'
                architect_result_row.error_message = ''
                rows_validated += 1
                architect_result_row.save()
            except Exception, e:
                import pdb; pdb.set_trace()
                logger.exception(e)
                architect_result_row.state = 'error'
                architect_result_row.error_message = e.message
                rows_failed += 1
                architect_result_row.save()
                continue
        
        if rows_failed > 0:
            self.upload_file.state = 'row_error'
        else:
            self.upload_file.state = 'validated'
        fail_msg = 'Failed to validate ' + str(rows_failed) + ' rows.'
        success_msg = 'Successfully validated ' + str(rows_validated) + ' rows.'
        
        self.upload_file.message += fail_msg + '\n' + success_msg + '\n'
        self.upload_file.save()

    def process(self, panel_id):
        from cephia.models import Specimen, Laboratory, Assay, Panels
        from assay.models import ArchitectResultRow, ArchitectResult, AssayResult
        
        rows_inserted = 0
        rows_failed = 0

        for architect_result_row in ArchitectResultRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            try:
                with transaction.atomic():
                    architect_result = ArchitectResult.objects.create(specimen=Specimen.objects.get(specimen_label=architect_result_row.specimen),
                                                                      assay=Assay.objects.get(name=architect_result_row.assay),
                                                                      sample_type=architect_result_row.sample_type,
                                                                      laboratory=Laboratory.objects.get(name=architect_result_row.site),
                                                                      test_date=self.float_as_date(float(architect_result_row.test_date)),
                                                                      operator=architect_result_row.operator,
                                                                      assay_kit_lot_id=architect_result_row.assay_kit_lot_id,
                                                                      plate_id=architect_result_row.plate_id,
                                                                      test_mode=architect_result_row.test_mode,
                                                                      well=architect_result_row.well,
                                                                      intermediate_1=architect_result_row.intermediate_1,
                                                                      intermediate_2=architect_result_row.intermediate_2,
                                                                      intermediate_3=architect_result_row.intermediate_3,
                                                                      intermediate_4=architect_result_row.intermediate_4,
                                                                      intermediate_5=architect_result_row.intermediate_5,
                                                                      intermediate_6=architect_result_row.intermediate_6,
                                                                      final_result=architect_result_row.final_result,
                                                                      panel_type=architect_result_row.panel_type)

                    AssayResult.objects.create(panel=Panels.objects.get(pk=panel_id),
                                               assay=Assay.objects.get(name=architect_result_row.assay),
                                               specimen=Specimen.objects.get(specimen_label=architect_result_row.specimen),
                                               test_date=self.float_as_date(float(architect_result_row.test_date)),
                                               result=architect_result_row.final_result)
                    
                    architect_result_row.state = 'processed'
                    architect_result_row.date_processed = timezone.now()
                    architect_result_row.error_message = ''
                    architect_result_row.save()
                    rows_inserted += 1

            except Exception, e:
                import pdb; pdb.set_trace()
                logger.exception(e)
                architect_result_row.state = 'error'
                architect_result_row.error_message = e.message
                architect_result_row.save()
                rows_failed += 1
                continue

        if rows_failed > 0:
            self.upload_file.state = 'row_error'
        else:
            self.upload_file.state = 'processed'
        fail_msg = 'Failed to process ' + str(rows_failed) + ' rows.'
        success_msg = 'Successfully processed ' + str(rows_inserted) + ' rows.'
        
        self.upload_file.message += fail_msg + '\n' + success_msg + '\n'
        self.upload_file.save()
