from file_handler import FileHandler
from handler_imports import *
import logging
from lib import log_exception

logger = logging.getLogger(__name__)

class BioPlexDukeFileHandler(FileHandler):
    upload_file = None

    def __init__(self, upload_file):
        super(BioPlexDukeFileHandler, self).__init__(upload_file)

        self.registered_columns = [
            'specimen_label',
            'specimen_purpose'
            'classification',
            
        ]

    def parse(self):
        from assay.models import BioPlexDukeResultRow

        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    self.header = [ x.strip() for x in self.header ]
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))

                    duke_result_row = BioPlexDukeResultRow.objects.create(
                        specimen_label = row_dict['specimen_label'],
                        specimen_purpose=row_dict['specimen_purpose'],
                        
                        classification=row_dict['classification'],
                        state='pending',
                        fileinfo=self.upload_file,
                        assay=self.upload_file.assay,
                        laboratory=None
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
        from assay.models import BioPlexDukeResultRow, BioPlexDukeResult, PanelMembership

        rows_validated = 0
        rows_failed = 0

        for duke_result_row in BioPlexDukeResultRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''

                panel = Panel.objects.get(pk=panel_id)
                try:
                    Specimen.objects.get(
                        specimen_label=duke_result_row.specimen_label,
                        specimen_type=panel.specimen_type,
                        parent_label__isnull=False
                    )
                except Specimen.DoesNotExist:
                    if duke_result_row.specimen_purpose == 'panel_specimen':
                        error_msg += "Specimen not recognised.\n"

                if error_msg:
                    raise Exception(error_msg)

                duke_result_row.state = 'validated'
                duke_result_row.error_message = ''
                rows_validated += 1
                duke_result_row.save()
            except Exception, e:
                raise
                logger.exception(e)
                duke_result_row.state = 'error'
                duke_result_row.error_message = e.message
                rows_failed += 1
                duke_result_row.save()
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
        from assay.models import BioPlexDukeResultRow, BioPlexDukeResult, AssayResult

        rows_inserted = 0
        rows_failed = 0

        for duke_result_row in BioPlexDukeResultRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            
            try:
                with transaction.atomic():
                    assay = assay_run.assay
                    panel = Panel.objects.get(pk=panel_id)
                    specimen = Specimen.objects.get(
                        specimen_label=duke_result_row.specimen_label,
                        specimen_type=panel.specimen_type,
                        parent_label__isnull=False
                    )

                    duke_result = BioPlexDukeResult.objects.create(
                        specimen=specimen,
                        assay=assay,
                        laboratory=assay_run.laboratory,
                        classification=duke_result_row.classification,
                        assay_run=assay_run,
                    )

                    if duke_result_row.classification is not None:
                        duke_result.recent = duke_result_row.classification == 'Recent'

                    final_result = None
                    if duke_result_row.classification is not None:
                        final_result = float(duke_result.recent)
                    
                    duke_result.save()

                    assay_result = AssayResult.objects.create(
                        panel=panel,
                        assay=assay,
                        specimen=specimen,
                        assay_run=assay_run,
                        result=final_result,
                        method='model_classification'
                    )
                    
                    duke_result.assay_result = assay_result
                    duke_result.save()
                    
                    duke_result_row.state = 'processed'
                    duke_result_row.date_processed = timezone.now()
                    duke_result_row.error_message = ''
                    duke_result_row.duke_result = duke_result
                    
                    duke_result_row.laboratory = assay_run.laboratory.name if assay_run.laboratory else None
                    
                    duke_result_row.save()
                    rows_inserted += 1

            except Exception, e:
                raise
                duke_result_row.state = 'error'
                duke_result_row.error_message = log_exception(e, logger)
                duke_result_row.save()
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
