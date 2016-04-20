from file_handler import FileHandler
from handler_imports import *
import logging

logger = logging.getLogger(__name__)

class LuminexFileHandler(FileHandler):
    upload_file = None

    def __init__(self, upload_file):
        super(LuminexFileHandler, self).__init__(upload_file)

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
                                   'result_gp120_n'
                                   'result_gp160_n',
                                   'result_gp41_n',
                                   'result_gp120_a',
                                   'result_gp160_a',
                                   'result_gp41_a',
                                   'result_LuminexIndex']


    def parse(self):
        from assay.models import LuminexResultRow

        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    self.header = [ x.strip() for x in self.header ]
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))

                    luminex_result_row = LuminexResultRow.objects.create(specimen_label=row_dict['specimen_label'],
                                                                         assay=row_dict['assay'],
                                                                         laboratory=row_dict['laboratory'],
                                                                         test_date=row_dict['test_date'],
                                                                         operator=row_dict['operator'],
                                                                         assay_kit_lot=row_dict['assay_kit_lot'],
                                                                         plate_identifier=row_dict['plate_identifier'],
                                                                         well=row_dict['well'],
                                                                         test_mode=row_dict['test_mode'],
                                                                         specimen_purpose=row_dict['specimen_purpose'],
                                                                         result_gp120_n=row_dict['result_gp120_n'],
                                                                         result_gp160_n=row_dict['result_gp160_n'],
                                                                         result_gp41_n=row_dict['result_gp41_n'],
                                                                         result_gp120_a=row_dict['result_gp120_a'],
                                                                         result_gp160_a=row_dict['result_gp160_a'],
                                                                         result_gp41_a=row_dict['result_gp41_a'],
                                                                         result_LuminexIndex=row_dict['result_LuminexIndex'],
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
        from assay.models import LuminexResultRow, LuminexResult, PanelMembership

        rows_validated = 0
        rows_failed = 0

        for luminex_result_row in LuminexResultRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''
                panel = Panel.objects.get(pk=panel_id)
                panel_memberhsips = PanelMembership.objects.filter(panel=panel)
                assay = Assay.objects.get(name=luminex_result_row.assay)

                try:
                    specimen = Specimen.objects.get(specimen_label=luminex_result_row.specimen_label,
                                                    specimen_type=panel.specimen_type,
                                                    parent_label__isnull=False)
                except Specimen.DoesNotExist:
                    error_msg += "Specimen not recognised.\n"

                # if specimen.visit.id not in [ membership.id for membership in panel_memberhsips ]:
                #     error_msg += "Specimen does not belong to any panel membership.\n"

                if error_msg:
                    raise Exception(error_msg)

                luminex_result_row.state = 'validated'
                luminex_result_row.error_message = ''
                rows_validated += 1
                luminex_result_row.save()
            except Exception, e:
                logger.exception(e)
                luminex_result_row.state = 'error'
                luminex_result_row.error_message = e.message
                rows_failed += 1
                luminex_result_row.save()
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
        from assay.models import LuminexResultRow, LuminexResult, AssayResult

        rows_inserted = 0
        rows_failed = 0

        for luminex_result_row in LuminexResultRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            try:
                with transaction.atomic():
                    assay = Assay.objects.get(name=luminex_result_row.assay)
                    panel = Panel.objects.get(pk=panel_id)
                    specimen = Specimen.objects.get(specimen_label=luminex_result_row.specimen_label,
                                                    specimen_type=panel.specimen_type,
                                                    parent_label__isnull=False)

                    assay_result = AssayResult.objects.create(panel=panel,
                                                              assay=assay,
                                                              specimen=specimen,
                                                              test_date=datetime.strptime(luminex_result_row.test_date, '%Y-%m-%d').date(),
                                                              result=luminex_result_row.result_LuminexIndex)

                    luminex_result = LuminexResult.objects.create(specimen=specimen,
                                                                  assay=assay,
                                                                  laboratory=Laboratory.objects.get(name=luminex_result_row.laboratory),
                                                                  test_date=datetime.strptime(luminex_result_row.test_date, '%Y-%m-%d').date(),
                                                                  operator=luminex_result_row.operator,
                                                                  assay_kit_lot=luminex_result_row.assay_kit_lot,
                                                                  plate_identifier=luminex_result_row.plate_identifier,
                                                                  test_mode=luminex_result_row.test_mode,
                                                                  well=luminex_result_row.well,
                                                                  specimen_purpose=luminex_result_row.specimen_purpose,
                                                                  result_gp120_n=luminex_result_row.result_gp120_n,
                                                                  result_gp160_n=luminex_result_row.result_gp160_n,
                                                                  result_gp41_n=luminex_result_row.result_gp41_n,
                                                                  result_gp120_a=luminex_result_row.result_gp120_a,
                                                                  result_gp160_a=luminex_result_row.result_gp160_a,
                                                                  result_gp41_a=luminex_result_row.result_gp41_a,
                                                                  result_LuminexIndex=luminex_result_row.result_LuminexIndex,
                                                                  assay_result=assay_result)

                    luminex_result_row.state = 'processed'
                    luminex_result_row.date_processed = timezone.now()
                    luminex_result_row.error_message = ''
                    luminex_result_row.save()
                    rows_inserted += 1

            except Exception, e:
                logger.exception(e)
                luminex_result_row.state = 'error'
                luminex_result_row.error_message = e.message
                luminex_result_row.save()
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
