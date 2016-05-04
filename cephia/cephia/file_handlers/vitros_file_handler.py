from file_handler import FileHandler
from handler_imports import *
import logging

logger = logging.getLogger(__name__)

class VitrosAvidityFileHandler(FileHandler):
    upload_file = None

    def __init__(self, upload_file):
        super(VitrosAvidityFileHandler, self).__init__(upload_file)

        self.registered_columns = ["specimen_label",
                                   "assay",
                                   "laboratory",
                                   "test_date",
                                   "operator",
                                   "assay_kit_lot",
                                   "well_treated_guanidine",
                                   "well_untreated_pbs",
                                   "test_mode",
                                   "specimen_purpose",
                                   "treated_guanidine_OD",
                                   "untreated_pbs_OD",
                                   "AI_reported",
                                   "AI",
                                   "panel",
                                   "interpretation"]

        self.assay_name = 'Vitros'

    def parse(self):
        from assay.models import VitrosAvidityResultRow

        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    self.header = [ x.strip() for x in self.header ]
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))

                    vitros_result_row = VitrosAvidityResultRow.objects.create(specimen_label=row_dict['specimen_label'],
                                                                              assay=row_dict['assay'],
                                                                              laboratory=row_dict['laboratory'],
                                                                              test_date=row_dict['test_date'],
                                                                              operator=row_dict['operator'],
                                                                              assay_kit_lot=row_dict['assay_kit_lot'],
                                                                              plate_identifier=row_dict['plate_identifier'],
                                                                              well_treated_guanidine=row_dict['well_treated_guanidine'],
                                                                              well_untreated_pbs=row_dict['well_untreated_pbs'],
                                                                              test_mode=row_dict['test_mode'],
                                                                              specimen_purpose=row_dict['specimen_purpose'],
                                                                              treated_guanidine_OD=row_dict["treated_guanidine_OD"],
                                                                              untreated_pbs_OD=row_dict["untreated_pbs_OD"],
                                                                              AI_reported=row_dict["AI_reported"],
                                                                              AI=row_dict["AI"],
                                                                              interpretation=row_dict["interpretation"],
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
        from assay.models import VitrosAvidityResultRow, VitrosAvidityResult, PanelMembership

        rows_validated = 0
        rows_failed = 0

        for vitros_result_row in VitrosAvidityResultRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''
                panel = Panel.objects.get(pk=panel_id)

                try:
                    specimen = Specimen.objects.get(specimen_label=vitros_result_row.specimen_label,
                                                    specimen_type=panel.specimen_type,
                                                    parent_label__isnull=False)
                except Specimen.DoesNotExist:
                    if vitros_result_row.specimen_purpose == 'panel_specimen':
                        error_msg += "Specimen not recognised.\n"

                if error_msg:
                    raise Exception(error_msg)

                # if specimen.visit.id not in [ membership.id for membership in panel_memberhsips ]:
                #     error_msg += "Specimen does not belong to any panel membership.\n"

                vitros_result_row.state = 'validated'
                vitros_result_row.error_message = ''
                rows_validated += 1
                vitros_result_row.save()
            except Exception, e:
                logger.exception(e)
                vitros_result_row.state = 'error'
                vitros_result_row.error_message = e.message
                rows_failed += 1
                vitros_result_row.save()
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
        from assay.models import VitrosAvidityResultRow, VitrosAvidityResult, AssayResult, PanelMembership

        rows_inserted = 0
        rows_failed = 0

        assay = Assay.objects.get(name=self.assay_name)
        panel = Panel.objects.get(pk=panel_id)
        panel_memberhsips = PanelMembership.objects.filter(panel=panel)
        panel_memberhsip_ids = [ membership.id for membership in panel_memberhsips ]

        for vitros_result_row in VitrosAvidityResultRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            try:
                warning_msg = ''

                with transaction.atomic():
                    specimen = None
                    try:
                        specimen = Specimen.objects.get(specimen_label=vitros_result_row.specimen_label,
                                                        specimen_type=panel.specimen_type,
                                                        parent_label__isnull=False)
                    except Specimen.DoesNotExist:
                        warning_msg += "Specimen not recognised.\n"

                    # if specimen.visit.id not in panel_memberhsip_ids:
                    #     warning_msg += "Specimen does not belong to any panel membership.\n"

                    vitros_result = VitrosAvidityResult.objects.create(specimen=specimen,
                                                                       assay=assay,
                                                                       laboratory=Laboratory.objects.get(name=vitros_result_row.laboratory),
                                                                       test_date=datetime.strptime(vitros_result_row.test_date, '%Y-%m-%d').date(),
                                                                       operator=vitros_result_row.operator,
                                                                       assay_kit_lot=vitros_result_row.assay_kit_lot,
                                                                       plate_identifier=vitros_result_row.plate_identifier,
                                                                       test_mode=vitros_result_row.test_mode,
                                                                       well_treated_guanidine=vitros_result_row.well_treated_guanidine,
                                                                       well_untreated_pbs=vitros_result_row.well_untreated_pbs,
                                                                       specimen_purpose=vitros_result_row.specimen_purpose,
                                                                       treated_guanidine_OD=vitros_result_row.treated_guanidine_OD or None,
                                                                       untreated_pbs_OD=vitros_result_row.untreated_pbs_OD or None,
                                                                       AI_reported=vitros_result_row.AI_reported or None,
                                                                       AI=vitros_result_row.AI or None,
                                                                       interpretation=vitros_result_row.interpretation,
                                                                       assay_run=assay_run)

                    vitros_result_row.state = 'processed'
                    vitros_result_row.date_processed = timezone.now()
                    vitros_result_row.error_message = ''
                    vitros_result_row.save()
                    rows_inserted += 1

            except Exception, e:
                logger.exception(e)
                vitros_result_row.state = 'error'
                vitros_result_row.error_message = e.message
                vitros_result_row.save()
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
