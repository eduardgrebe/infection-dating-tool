from file_handler import FileHandler
from handler_imports import *
import logging

logger = logging.getLogger(__name__)

class BioRadAvidityJHUFileHandler(FileHandler):
    upload_file = None

    def __init__(self, upload_file):
        super(BioRadAvidityJHUFileHandler, self).__init__(upload_file)

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
                                   'result_treated_OD',
                                   'result_untreated_OD',
                                   'result_AI',
                                   'result_AI_recalc']


    def parse(self):
        from assay.models import BioRadAvidityJHUResultRow

        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    self.header = [ x.strip() for x in self.header ]
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))

                    biorad_result_row = BioRadAvidityJHUResultRow.objects.create(specimen_label=row_dict['specimen_label'],
                                                                                    assay=row_dict['assay'],
                                                                                    laboratory=row_dict['laboratory'],
                                                                                    test_date=row_dict['test_date'],
                                                                                    operator=row_dict['operator'],
                                                                                    assay_kit_lot=row_dict['assay_kit_lot'],
                                                                                    plate_identifier=row_dict['plate_identifier'],
                                                                                    well=row_dict['well'],
                                                                                    test_mode=row_dict['test_mode'],
                                                                                    specimen_purpose=row_dict['specimen_purpose'],
                                                                                    result_treated_OD=row_dict['result_treated_OD'],
                                                                                    result_untreated_OD=row_dict['result_untreated_OD'],
                                                                                    result_AI=row_dict['result_AI'],
                                                                                    result_AI_recalc=row_dict['result_AI_recalc'],
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

    def validate(self, panel_id):
        from cephia.models import Specimen, Panel, Assay
        from assay.models import BioRadAvidityJHUResultRow, BioRadAvidityJHUResult, PanelMembership

        rows_validated = 0
        rows_failed = 0

        for biorad_result_row in BioRadAvidityJHUResultRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''
                panel = Panel.objects.get(pk=panel_id)
                panel_memberhsips = PanelMembership.objects.filter(panel=panel)
                assay = Assay.objects.get(name=biorad_result_row.assay)

                try:
                    specimen = Specimen.objects.get(specimen_label=biorad_result_row.specimen_label,
                                                    specimen_type=panel.specimen_type,
                                                    parent_label__isnull=False)
                except Specimen.DoesNotExist:
                    error_msg += "Specimen not recognised.\n"

                # if specimen.visit.id not in [ membership.id for membership in panel_memberhsips ]:
                #     error_msg += "Specimen does not belong to any panel membership.\n"

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

    def process(self, panel_id):
        from cephia.models import Specimen, Laboratory, Assay, Panel
        from assay.models import BioRadAvidityJHUResultRow, BioRadAvidityJHUResult, AssayResult

        rows_inserted = 0
        rows_failed = 0

        for biorad_result_row in BioRadAvidityJHUResultRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            try:
                with transaction.atomic():
                    assay = Assay.objects.get(name=biorad_result_row.assay)
                    panel = Panel.objects.get(pk=panel_id)
                    specimen = Specimen.objects.get(specimen_label=biorad_result_row.specimen_label,
                                                    specimen_type=panel.specimen_type,
                                                    parent_label__isnull=False)

                    assay_result = AssayResult.objects.create(panel=panel,
                                                              assay=assay,
                                                              specimen=specimen,
                                                              test_date=datetime.strptime(biorad_result_row.test_date, '%Y-%m-%d').date(),
                                                              result=biorad_result_row.result_AI)

                    biorad_result = BioRadAvidityJHUResult.objects.create(specimen=specimen,
                                                                          assay=assay,
                                                                          laboratory=Laboratory.objects.get(name=biorad_result_row.laboratory),
                                                                          test_date=datetime.strptime(biorad_result_row.test_date, '%Y-%m-%d').date(),
                                                                          operator=biorad_result_row.operator,
                                                                          assay_kit_lot=biorad_result_row.assay_kit_lot,
                                                                          plate_identifier=biorad_result_row.plate_identifier,
                                                                          test_mode=biorad_result_row.test_mode,
                                                                          well=biorad_result_row.well,
                                                                          specimen_purpose=biorad_result_row.specimen_purpose,
                                                                          result_treated_OD=biorad_result_row.result_treated_OD,
                                                                          result_untreated_OD=biorad_result_row.result_untreated_OD,
                                                                          result_AI=biorad_result_row.result_AI,
                                                                          result_AI_recalc=biorad_result_row.result_AI_recalc,
                                                                          assay_result=assay_result)

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
