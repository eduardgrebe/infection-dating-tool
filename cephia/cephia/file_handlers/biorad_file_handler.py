from file_handler import FileHandler
from handler_imports import *
import logging

logger = logging.getLogger(__name__)

class BioRadFileHandler(FileHandler):
    upload_file = None

    def __init__(self, upload_file):
        super(BioRadFileHandler, self).__init__(upload_file)

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
                                   'result_treated_well_OD',
                                   'result_untreated_well_OD',
                                   'result_AI']


    def parse(self):
        from assay.models import BioradResultRow

        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    
                    biorad_result_row = BioradResultRow.objects.create(specimen=row_dict['Specimen ID'],
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
        from assay.models import BioradResultRow, BioradResult
        
        rows_validated = 0
        rows_failed = 0
        
        for biorad_result_row in BioradResultRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''
                
                # try:
                #     Specimen.objects.get(pk=biorad_result_row.specimen)
                # except Specimen.DoesNotExist:
                #     error_msg += "Specimen not recognised.\n"

                # try:
                #     Panel.objects.get(pk=biorad_result_row.panel)
                # except Panel.DoesNotExist:
                #     error_msg += "Panel not recognised.\n"

                if error_msg:
                    raise Exception(error_msg)
                
                biorad_result_row.state = 'validated'
                biorad_result_row.error_message = ''
                rows_validated += 1
                biorad_result_row.save()
            except Exception, e:
                logger.exception(e)
                biorad_result_row.state = 'error'
                biorad_result_row.error_message = e.message
                rows_failed += 1
                biorad_result_row.save()
                continue
        
        if rows_failed > 0:
            self.upload_file.state = 'row_error'
        else:
            self.upload_file.state = 'validated'
        fail_msg = 'Failed to validate ' + str(rows_failed) + ' rows.'
        success_msg = 'Successfully validated ' + str(rows_validated) + ' rows.'
        
        self.upload_file.message += fail_msg + '\n' + success_msg + '\n'
        self.upload_file.save()

    def process(self):
        from cephia.models import Specimen
        from assay.models import BioradResultRow, BioradResult
        
        rows_inserted = 0
        rows_failed = 0

        for biorad_result_row in BioradResultRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            try:
                with transaction.atomic():
                    biorad_result = BioradResult.objects.create(specimen=Specimen.objects.get(pk=biorad_result_row.specimen),
                                                                assay=Assay.objects.get(pk=biorad_result_row.assay),
                                                                sample_type=biorad_result_row.sample_type,
                                                                site=Site.objects.get(name=biorad_result_row.site),
                                                                test_date=self.registered_dates(),
                                                                operator=biorad_result_row.operator,
                                                                assay_kit_lot_id=biorad_result_row.assay_kit_lot_id,
                                                                plate_id=biorad_result_row.plate_id,
                                                                test_mode=biorad_result_row.test_mode,
                                                                well=biorad_result_row.well,
                                                                intermediate_1=biorad_result_row.intermediate_1,
                                                                intermediate_2=biorad_result_row.intermediate_2,
                                                                intermediate_3=biorad_result_row.intermediate_3,
                                                                intermediate_4=biorad_result_row.intermediate_4,
                                                                intermediate_5=biorad_result_row.intermediate_5,
                                                                intermediate_6=biorad_result_row.intermediate_6,
                                                                final_result=biorad_result_row.final_result,
                                                                panel_type=biorad_result_row.panel_type)
                    
                    biorad_result_row.state = 'processed'
                    biorad_result_row.date_processed = timezone.now()
                    biorad_result_row.error_message = ''
                    biorad_result_row.save()
                    rows_inserted += 1

            except Exception, e:
                logger.exception(e)
                biorad_result_row.state = 'error'
                biorad_result_row.error_message = e.message
                biorad_result_row.save()
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
