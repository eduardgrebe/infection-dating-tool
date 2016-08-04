from file_handler import FileHandler
from handler_imports import *
import logging
from lib import log_exception

logger = logging.getLogger(__name__)

class ISGlobalFileHandler(FileHandler):
    upload_file = None

    def __init__(self, upload_file):
        super(ISGlobalFileHandler, self).__init__(upload_file)

        self.registered_columns = [
            'specimen_label',
            'specimen_purpose'
            'classification_weighted_model',
            'classification_unweighted_model',
            
        ]

    def parse(self):
        from assay.models import ISGlobalResultRow

        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    self.header = [ x.strip() for x in self.header ]
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))

                    isg_result_row = ISGlobalResultRow.objects.create(
                        specimen_label = row_dict['specimen_label'],
                        specimen_purpose=row_dict['specimen_purpose'],
                        
                        classification_weighted_model=row_dict['classification_weighted_model'],
                        classification_unweighted_model=row_dict['classification_unweighted_model'],
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
        from assay.models import ISGlobalResultRow, ISGlobalResult, PanelMembership

        rows_validated = 0
        rows_failed = 0

        for isg_result_row in ISGlobalResultRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''

                panel = Panel.objects.get(pk=panel_id)
                try:
                    Specimen.objects.get(
                        specimen_label=isg_result_row.specimen_label,
                        specimen_type=panel.specimen_type,
                        parent_label__isnull=False
                    )
                except Specimen.DoesNotExist:
                    if isg_result_row.specimen_purpose == 'panel_specimen':
                        error_msg += "Specimen not recognised.\n"

                if error_msg:
                    raise Exception(error_msg)

                isg_result_row.state = 'validated'
                isg_result_row.error_message = ''
                rows_validated += 1
                isg_result_row.save()
            except Exception, e:
                raise
                logger.exception(e)
                isg_result_row.state = 'error'
                isg_result_row.error_message = e.message
                rows_failed += 1
                isg_result_row.save()
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
        from assay.models import ISGlobalResultRow, ISGlobalResult, AssayResult

        rows_inserted = 0
        rows_failed = 0

        for isg_result_row in ISGlobalResultRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            
            try:
                with transaction.atomic():
                    assay = assay_run.assay
                    panel = Panel.objects.get(pk=panel_id)
                    specimen = Specimen.objects.get(
                        specimen_label=isg_result_row.specimen_label,
                        specimen_type=panel.specimen_type,
                        parent_label__isnull=False
                    )

                    isg_result = ISGlobalResult.objects.create(
                        specimen=specimen,
                        assay=assay,
                        laboratory=assay_run.laboratory,
                        classification_weighted_model=isg_result_row.classification_weighted_model,
                        classification_unweighted_model=isg_result_row.classification_unweighted_model,
                        assay_run=assay_run,
                    )

                    if isg_result_row.classification_weighted_model is not None:
                        isg_result.recent_weighted_model = isg_result_row.classification_weighted_model == 'Recent'

                    final_result = None
                    if isg_result_row.classification_unweighted_model is not None:
                        isg_result.recent_unweighted_model = isg_result_row.classification_unweighted_model == 'Recent'
                        final_result = float(isg_result.recent_unweighted_model)

                    
                    isg_result.save()

                    assay_result = AssayResult.objects.create(
                        panel=panel,
                        assay=assay,
                        specimen=specimen,
                        assay_run=assay_run,
                        result=final_result,
                        method='unweighted_model_classification'
                    )
                    
                    isg_result.assay_result = assay_result
                    isg_result.save()
                    
                    isg_result_row.state = 'processed'
                    isg_result_row.date_processed = timezone.now()
                    isg_result_row.error_message = ''
                    isg_result_row.isg_result = isg_result
                    
                    isg_result_row.laboratory = assay_run.laboratory.name if assay_run.laboratory else None
                    
                    isg_result_row.save()
                    rows_inserted += 1

            except Exception, e:
                raise
                isg_result_row.state = 'error'
                isg_result_row.error_message = log_exception(e, logger)
                isg_result_row.save()
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
