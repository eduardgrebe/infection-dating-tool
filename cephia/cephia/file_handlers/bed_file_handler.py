from file_handler import FileHandler
from handler_imports import *
import logging

logger = logging.getLogger(__name__)

class BEDFileHandler(FileHandler):
    upload_file = None
    
    def __init__(self, upload_file):
        super(BEDFileHandler, self).__init__(upload_file)

        self.registered_columns = ['specimen_label',
                                   'assay',
                                   'laboratory',
                                   'test_date',
                                   'operator',
                                   'assay_kit_lot',
                                   'plate_identifier',
                                   'well',
                                   'test_mode',
                                   'specimen_purpose',
                                   'result_OD',
                                   'result_calibrator_OD',
                                   'result_ODn',
                                   'panel_type']

    def parse(self):
        from assay.models import BEDResultRow
        
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    self.header = [ x.strip() for x in self.header ]
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))

                    bed_result_row = BEDResultRow.objects.create(specimen_label=row_dict['specimen_label'],
                                                                 assay=row_dict['assay'],
                                                                 laboratory=row_dict['laboratory'],
                                                                 test_date=row_dict['test_date'],
                                                                 operator=row_dict['operator'],
                                                                 assay_kit_lot=row_dict['assay_kit_lot'],
                                                                 plate_identifier=row_dict['plate_identifier'],
                                                                 test_mode=row_dict['test_mode'],
                                                                 well=row_dict['well'],
                                                                 specimen_purpose=row_dict['specimen_purpose'],
                                                                 result_OD=row_dict['result_OD'],
                                                                 result_calibrator_OD=row_dict['result_calibrator_OD'],
                                                                 result_ODn=row_dict['result_ODn'],
                                                                 panel_type=row_dict['panel_type'],
                                                                 state='pending',
                                                                 fileinfo=self.upload_file)


                    rows_inserted += 1
            except Exception, e:
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
        from cephia.models import Specimen, Assay, Panel
        from assay.models import BEDResultRow

        rows_validated = 0
        rows_failed = 0
        
        for bed_result_row in BEDResultRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''
                
                # try:
                #     Specimen.objects.get(pk=bed_result_row.specimen)
                # except Specimen.DoesNotExist:
                #     error_msg += "Specimen not recognised.\n"

                # try:
                #     Panel.objects.get(pk=bed_result_row.panel)
                # except Panel.DoesNotExist:
                #     error_msg += "Panel not recognised.\n"

                if error_msg:
                    raise Exception(error_msg)
                
                bed_result_row.state = 'validated'
                bed_result_row.error_message = ''
                rows_validated += 1
                bed_result_row.save()
            except Exception, e:
                logger.exception(e)
                bed_result_row.state = 'error'
                bed_result_row.error_message = e.message
                rows_failed += 1
                bed_result_row.save()
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
        from assay.models import BEDResultRow, BEDResult, AssayResult
        
        rows_inserted = 0
        rows_failed = 0

        for bed_result_row in BEDResultRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            try:
                with transaction.atomic():
                    bed_result = BEDResult.objects.create(specimen=Specimen.objects.get(specimen_label=bed_result_row.specimen),
                                                          assay=Assay.objects.get(name=bed_result_row.assay),
                                                          sample_type=bed_result_row.sample_type,
                                                          laboratory=Laboratory.objects.get(name=bed_result_row.site),
                                                          test_date=self.float_as_date(float(bed_result_row.test_date)),
                                                          operator=bed_result_row.operator,
                                                          assay_kit_lot_id=bed_result_row.assay_kit_lot_id,
                                                          plate_id=bed_result_row.plate_id,
                                                          test_mode=bed_result_row.test_mode,
                                                          well=bed_result_row.well,
                                                          intermediate_1=bed_result_row.intermediate_1,
                                                          intermediate_2=bed_result_row.intermediate_2,
                                                          intermediate_3=bed_result_row.intermediate_3,
                                                          intermediate_4=bed_result_row.intermediate_4,
                                                          intermediate_5=bed_result_row.intermediate_5,
                                                          intermediate_6=bed_result_row.intermediate_6,
                                                          final_result=bed_result_row.final_result,
                                                          panel_type=bed_result_row.panel_type)

                    AssayResult.objects.create(panel=Panels.objects.get(pk=panel_id),
                                               assay=Assay.objects.get(name=bed_result_row.assay),
                                               specimen=Specimen.objects.get(specimen_label=bed_result_row.specimen),
                                               test_date=self.float_as_date(float(bed_result_row.test_date)),
                                               result=bed_result_row.final_result)
                    
                    bed_result_row.state = 'processed'
                    bed_result_row.date_processed = timezone.now()
                    bed_result_row.error_message = ''
                    bed_result_row.save()
                    rows_inserted += 1

            except Exception, e:
                logger.exception(e)
                bed_result_row.state = 'error'
                bed_result_row.error_message = e.message
                bed_result_row.save()
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
