from file_handler import FileHandler
from handler_imports import *
import logging
from lib import log_exception

logger = logging.getLogger(__name__)

class CustomAssayFileHandler(FileHandler):
    upload_file = None

    def __init__(self, upload_file):
        super(CustomAssayFileHandler, self).__init__(upload_file)

        self.registered_columns = [
            'specimen_label',
            'assay',
            'laboratory',
            'test_date',
            'operator',
            'assay_kit_lot',
            'plate_identifier',
            'test_mode',
            'specimen_purpose',
            'classification'
        ]

    def parse(self):
        from assay.models import CustomAssayResultRow

        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    self.header = [ x.strip() for x in self.header ]
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))

                    custom_assay_result_row = CustomAssayResultRow.objects.create(
                        specimen_label = row_dict.get('specimen_label'),
                        assay = row_dict.get('assay'),
                        laboratory = row_dict.get('laboratory'),
                        test_date = row_dict.get('test_date'),
                        operator = row_dict.get('operator'),
                        assay_kit_lot = row_dict.get('assay_kit_lot'),
                        plate_identifier = row_dict.get('plate_identifier'),
                        test_mode = row_dict.get('test_mode'),
                        specimen_purpose=row_dict.get('specimen_purpose'),
                        classification=row_dict['classification'],
                        state='pending',
                        fileinfo=self.upload_file
                    )

                    rows_inserted += 1
            except Exception, e:
                raise
                self.upload_file.message = "row " + str(row_num) + ": " + log_exception(e, logger)
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

    def validate(self, panel_id):
        from cephia.models import Specimen, Panel, Assay
        from assay.models import CustomAssayResultRow, CustomAssayResult, PanelMembership

        rows_validated = 0
        rows_failed = 0

        for custom_assay_result_row in CustomAssayResultRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''

                panel = Panel.objects.get(pk=panel_id)
                try:
                    Specimen.objects.get(
                        specimen_label=custom_assay_result_row.specimen_label,
                        specimen_type=panel.specimen_type,
                        parent_label__isnull=False
                    )
                except Specimen.DoesNotExist:
                    if custom_assay_result_row.specimen_purpose == 'panel_specimen':
                        error_msg += "Specimen not recognised.\n"

                if error_msg:
                    raise Exception(error_msg)

                custom_assay_result_row.state = 'validated'
                custom_assay_result_row.error_message = ''
                rows_validated += 1
                custom_assay_result_row.save()
            except Exception, e:
                raise
                logger.exception(e)
                custom_assay_result_row.state = 'error'
                custom_assay_result_row.error_message = e.message
                rows_failed += 1
                custom_assay_result_row.save()
                continue

        if rows_failed > 0:
            self.upload_file.state = 'row_error'
        else:
            self.upload_file.state = 'validated'
        fail_msg = 'Failed to validate ' + str(rows_failed) + ' rows.'
        success_msg = 'Successfully validated ' + str(rows_validated) + ' rows.'

        self.upload_file.message += fail_msg + '\n' + success_msg + '\n'
        self.upload_file.save()

    def process(self, panel_id, assay_run):
        from cephia.models import Specimen, Laboratory, Assay, Panel
        from assay.models import CustomAssayResultRow, CustomAssayResult, AssayResult

        rows_inserted = 0
        rows_failed = 0

        for custom_assay_result_row in CustomAssayResultRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            
            try:
                with transaction.atomic():
                    assay = assay_run.assay # assay = Assay.objects.get(name=self.assay_name) which one?
                    panel = Panel.objects.get(pk=panel_id)
                    specimen = Specimen.objects.get(
                        specimen_label=custom_assay_result_row.specimen_label,
                        specimen_type=panel.specimen_type,
                        parent_label__isnull=False
                    )

                    try:
                        laboratory = Laboratory.objects.get(name=custom_assay_result_row.laboratory)
                    except Laboratory.DoesNotExist:
                        laboratory = self.upload_file.laboratory

                    test_date = None
                    if custom_assay_result_row.test_date:
                        test_date = datetime.strptime(custom_assay_result_row.test_date, '%Y-%m-%d').date()

                    custom_assay_result = CustomAssayResult.objects.create(
                        specimen=specimen,
                        assay=assay,
                        laboratory=laboratory,
                        test_date=test_date,
                        operator=custom_assay_result_row.operator,
                        assay_kit_lot=custom_assay_result_row.assay_kit_lot,
                        plate_identifier=custom_assay_result_row.plate_identifier,
                        test_mode=custom_assay_result_row.test_mode,
                        specimen_purpose=custom_assay_result_row.specimen_purpose,
                        classification=custom_assay_result_row.classification,
                        assay_run=assay_run
                    )

                    if custom_assay_result_row.classification is not None:
                        custom_assay_result.recent = custom_assay_result_row.classification.lower() == 'recent'

                    final_result = None
                    if custom_assay_result_row.classification is not None:
                        final_result = float(custom_assay_result.recent)
                    
                    custom_assay_result.save()

                    assay_result = AssayResult.objects.create(
                        panel=panel,
                        assay=assay,
                        specimen=specimen,
                        test_date=test_date,
                        assay_run=assay_run,
                        result=final_result,
                        method='model_classification'
                    )
                    
                    custom_assay_result.assay_result = assay_result
                    custom_assay_result.save()
                    
                    custom_assay_result_row.state = 'processed'
                    custom_assay_result_row.date_processed = timezone.now()
                    custom_assay_result_row.error_message = ''
                    custom_assay_result_row.custom_result = custom_assay_result
                    
                    custom_assay_result_row.laboratory = assay_run.laboratory.name if assay_run.laboratory else None
                    
                    custom_assay_result_row.save()
                    rows_inserted += 1

            except Exception, e:
                custom_assay_result_row.state = 'error'
                custom_assay_result_row.error_message = log_exception(e, logger)
                custom_assay_result_row.save()
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
