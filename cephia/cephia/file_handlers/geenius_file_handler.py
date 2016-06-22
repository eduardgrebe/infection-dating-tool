from file_handler import FileHandler
from handler_imports import *
import logging
from lib import log_exception

logger = logging.getLogger(__name__)

class GeeniusFileHandler(FileHandler):
    upload_file = None

    def __init__(self, upload_file):
        super(GeeniusFileHandler, self).__init__(upload_file)

        self.registered_columns = [
            'specimen_label',
            'assay',
            'laboratory',
            'test_date',
            'assay_kit_lot',
            'plate_identifier',
            'test_mode',
            'specimen_purpose',
            
            'gp36_bi',
            'gp140_bi',
            'p31_bi',
            'gp160_bi',
            'p24_bi',
            'gp41_bi',
            'ctrl_bi',
            'GeeniusIndex',
            'exclusion',
            'interpretation',
        ]

    def parse(self):
        from assay.models import GeeniusResultRow

        rows_inserted = 0
        rows_failed = 0
        valid_columns = set(self.registered_columns)

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    self.header = [ x.strip() for x in self.header ]
                    row_dict = dict((k,v) for (k,v) in zip(self.header, self.file_rows[row_num]) if k in valid_columns)

                    GeeniusResultRow.objects.create(
                        state='pending',
                        fileinfo=self.upload_file,
                        **row_dict
                    )

                    rows_inserted += 1
            except Exception, e:
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
        from assay.models import GeeniusResultRow, GeeniusResult, PanelMembership

        rows_validated = 0
        rows_failed = 0

        for geenius_result_row in GeeniusResultRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''
                panel = Panel.objects.get(pk=panel_id)

                try:
                    Specimen.objects.get(
                        specimen_label=geenius_result_row.specimen_label,
                        specimen_type=panel.specimen_type,
                        parent_label__isnull=False)
                except Specimen.DoesNotExist:
                    if geenius_result_row.specimen_purpose != 'panel_specimen':
                        error_msg += "Specimen not recognised.\n"

                # if specimen.visit.id not in [ membership.id for membership in panel_memberhsips ]:
                #     error_msg += "Specimen does not belong to any panel membership.\n"

                if error_msg:
                    raise Exception(error_msg)

                geenius_result_row.state = 'validated'
                geenius_result_row.error_message = ''
                rows_validated += 1
                geenius_result_row.save()
            except Exception, e:
                geenius_result_row.state = 'error'
                geenius_result_row.error_message = log_exception(e, logger)
                rows_failed += 1
                geenius_result_row.save()
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
        from assay.models import GeeniusResultRow, GeeniusResult, AssayResult

        rows_inserted = 0
        rows_failed = 0

        for geenius_result_row in GeeniusResultRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            try:
                with transaction.atomic():
                    assay = Assay.objects.get(name=geenius_result_row.assay)
                    panel = Panel.objects.get(pk=panel_id)
                    specimen = Specimen.objects.get(
                        specimen_label=geenius_result_row.specimen_label,
                        specimen_type=panel.specimen_type,
                        parent_label__isnull=False)

                    warning_msg = ''
                    try:
                        is_excluded = bool(int(geenius_result_row.exclusion))
                    except (ValueError, TypeError):
                        warning_msg += 'exclusion could not be converted to an integer'
                        is_excluded = True

                    try:
                        final_result = float(geenius_result_row.GeeniusIndex)
                    except (ValueError, TypeError):
                        final_result = None
                        warning_msg += 'GeeniusIndex could not be converted to a float'


                    try:
                        result_columns = ['gp41_bi', 'gp160_bi', 'p31_bi']
                        result_sum = sum([float(getattr(geenius_result_row, column)) for column in result_columns])
                        final_result = result_sum / float(geenius_result_row.ctrl_bi)
                    except Exception, e:
                        warning_msg += 'Could not recalc: ' + log_exception(e)
                        final_result = None
                    
                    assay_result = AssayResult.objects.create(
                        panel=panel,
                        assay=assay,
                        specimen=specimen,
                        test_date=datetime.strptime(geenius_result_row.test_date, '%Y-%m-%d').date(),
                        warning_msg=warning_msg,
                        assay_run=assay_run,
                        result=None if is_excluded else final_result
                    )
                    

                    geenius_result = GeeniusResult.objects.create(
                        specimen=specimen,
                        assay=assay,
                        laboratory=Laboratory.objects.get(name=geenius_result_row.laboratory),
                        test_date=datetime.strptime(geenius_result_row.test_date, '%Y-%m-%d').date(),
                        operator=geenius_result_row.operator,
                        assay_kit_lot=geenius_result_row.assay_kit_lot,
                        plate_identifier=geenius_result_row.plate_identifier,
                        test_mode=geenius_result_row.test_mode,

                        gp36_bi = geenius_result_row.gp36_bi,
                        gp140_bi = geenius_result_row.gp140_bi,
                        gp160_bi = geenius_result_row.gp160_bi,
                        p24_bi = geenius_result_row.p24_bi,
                        gp41_bi = geenius_result_row.gp41_bi,
                        ctrl_bi = geenius_result_row.ctrl_bi,
                        
                        GeeniusIndex = final_result,
                        
                        exclusion = geenius_result_row.exclusion,
                        interpretation = geenius_result_row.interpretation,
                        assay_result=assay_result,
                        assay_run=assay_run
                    )

                    geenius_result_row.state = 'processed'
                    geenius_result_row.date_processed = timezone.now()
                    geenius_result_row.error_message = ''
                    geenius_result_row.geenius_result = geenius_result
                    geenius_result_row.save()
                    rows_inserted += 1

            except Exception, e:
                logger.exception(e)
                geenius_result_row.state = 'error'
                geenius_result_row.error_message = e.message
                geenius_result_row.save()
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
