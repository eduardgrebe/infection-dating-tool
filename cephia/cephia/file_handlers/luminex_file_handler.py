from django.db.models.functions import Length, Substr, Lower
from file_handler import FileHandler
from handler_imports import *
import logging
import algorithms
from lib import log_exception

logger = logging.getLogger(__name__)

class LuminexFileHandler(FileHandler):
    upload_file = None

    def __init__(self, upload_file):
        super(LuminexFileHandler, self).__init__(upload_file)

        self.registered_columns = ["assay",
                                   "panel",
                                   "laboratory",
                                   "operator",
                                   "plate_identifier",
                                   "test_date",
                                   "assay_kit_lot",
                                   "test_mode",
                                   "specimen_purpose",
                                   "specimen_label",
                                   "well_untreated",
                                   "well_treated",
                                   "BSA_MFI",
                                   "IgG_MFI",
                                   "gp120_MFI",
                                   "gp160_MFI",
                                   "gp41_MFI",
                                   "BSA_MFImb",
                                   "IgG_MFImb",
                                   "gp120_MFImb",
                                   "gp160_MFImb",
                                   "gp41_MFImb",
                                   "calibrator_BSA",
                                   "calibrator_IgG",
                                   "calibrator_gp120",
                                   "calibrator_gp160",
                                   "calibrator_gp41",
                                   "gp120_MFIn",
                                   "gp160_MFIn",
                                   "gp41_MFIn",
                                   "DEA_treated_BSA_MFI",
                                   "DEA_treated_IgG_MFI",
                                   "DEA_treated_gp120_MFI",
                                   "DEA_treated_gp160_MFI",
                                   "DEA_treated_gp41_MFI",
                                   "DEA_treated_BSA_MFImb",
                                   "DEA_treated_IgG_MFImb",
                                   "DEA_treated_gp120_MFImb",
                                   "DEA_treated_gp160_MFImb",
                                   "DEA_treated_gp41_MFImb",
                                   "DEA_treated_gp120_MFIn",
                                   "DEA_treated_gp160_MFIn",
                                   "DEA_treated_gp41_MFIn",
                                   "gp120_AI",
                                   "gp160_AI",
                                   "gp41_AI"]

        self.assay_name = 'BioPlex-CDC'

    def parse(self):
        from assay.models import LuminexCDCResultRow

        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    self.header = [ x.strip() for x in self.header ]
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))

                    luminex_result_row = LuminexCDCResultRow.objects.create(
                        assay=row_dict["assay"],
                                                                            laboratory=row_dict["laboratory"],
                        operator=row_dict["operator"],
                        plate_identifier=row_dict["plate_identifier"],
                        test_date=row_dict["test_date"],
                        assay_kit_lot=row_dict["assay_kit_lot"],
                        test_mode=row_dict["test_mode"],
                        specimen_purpose=row_dict["specimen_purpose"],
                        specimen_label=row_dict["specimen_label"],
                        well_untreated=row_dict["well_untreated"],
                        well_treated=row_dict["well_treated"],
                        BSA_MFI=row_dict["BSA_MFI"],
                        IgG_MFI=row_dict["IgG_MFI"],
                        gp120_MFI=row_dict["gp120_MFI"],
                        gp160_MFI=row_dict["gp160_MFI"],
                        gp41_MFI=row_dict["gp41_MFI"],
                        BSA_MFImb=row_dict["BSA_MFImb"],
                        IgG_MFImb=row_dict["IgG_MFImb"],
                        gp120_MFImb=row_dict["gp120_MFImb"],
                        gp160_MFImb=row_dict["gp160_MFImb"],
                        gp41_MFImb=row_dict["gp41_MFImb"],
                        calibrator_BSA=row_dict["calibrator_BSA"],
                        calibrator_IgG=row_dict["calibrator_IgG"],
                        calibrator_gp120=row_dict["calibrator_gp120"],
                        calibrator_gp160=row_dict["calibrator_gp160"],
                        calibrator_gp41=row_dict["calibrator_gp41"],
                        gp120_MFIn=row_dict["gp120_MFIn"],
                        gp160_MFIn=row_dict["gp160_MFIn"],
                        gp41_MFIn=row_dict["gp41_MFIn"],
                        DEA_treated_BSA_MFI=row_dict["DEA_treated_BSA_MFI"],
                        DEA_treated_IgG_MFI=row_dict["DEA_treated_IgG_MFI"],
                        DEA_treated_gp120_MFI=row_dict["DEA_treated_gp120_MFI"],
                        DEA_treated_gp160_MFI=row_dict["DEA_treated_gp160_MFI"],
                        DEA_treated_gp41_MFI=row_dict["DEA_treated_gp41_MFI"],
                        DEA_treated_BSA_MFImb=row_dict["DEA_treated_BSA_MFImb"],
                        DEA_treated_IgG_MFImb=row_dict["DEA_treated_IgG_MFImb"],
                        DEA_treated_gp120_MFImb=row_dict["DEA_treated_gp120_MFImb"],
                        DEA_treated_gp160_MFImb=row_dict["DEA_treated_gp160_MFImb"],
                        DEA_treated_gp41_MFImb=row_dict["DEA_treated_gp41_MFImb"],
                        DEA_treated_gp120_MFIn=row_dict["DEA_treated_gp120_MFIn"],
                        DEA_treated_gp160_MFIn=row_dict["DEA_treated_gp160_MFIn"],
                        DEA_treated_gp41_MFIn=row_dict["DEA_treated_gp41_MFIn"],
                        gp120_AI=row_dict["gp120_AI"],
                        gp160_AI=row_dict["gp160_AI"],
                        gp41_AI=row_dict["gp41_AI"],
                        state='pending',
                        fileinfo=self.upload_file
                    )

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
        from assay.models import LuminexCDCResultRow, LuminexCDCResult, PanelMembership

        rows_validated = 0
        rows_failed = 0
        panel = Panel.objects.get(pk=panel_id)

        for luminex_result_row in LuminexCDCResultRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''
                try:
                    # need test_date and run for the lab
                    specimen = Specimen.objects.get(
                        specimen_label=luminex_result_row.specimen_label,
                        specimen_type=panel.specimen_type,
                        parent_label__isnull=False)
                except Specimen.DoesNotExist:
                    if luminex_result_row.specimen_purpose == "panel_specimen":
                        partial_matches = Specimen.objects.filter(
                            specimen_label__startswith=luminex_result_row.specimen_label[0:4],
                            specimen_type=panel.specimen_type,
                            parent_label__isnull=False)
                        if not partial_matches:
                            error_msg += "Specimen not recognised.\n"

                if error_msg:
                    raise Exception(error_msg)

                luminex_result_row.state = 'validated'
                luminex_result_row.error_message = ''
                rows_validated += 1
                luminex_result_row.save()
            except Exception, e:
                logger.exception(e)
                luminex_result_row.state = 'error'
                luminex_result_row.error_message = log_exception(e, logger)
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

    def process(self, panel_id, assay_run):
        from cephia.models import Specimen, Laboratory, Assay, Panel
        from assay.models import LuminexCDCResultRow, LuminexCDCResult, AssayResult, PanelMembership

        rows_inserted = 0
        rows_failed = 0

        assay = Assay.objects.get(name=self.assay_name)
        panel = Panel.objects.get(pk=panel_id)

        for luminex_result_row in LuminexCDCResultRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            try:
                warning_msg = ''
                with transaction.atomic():
                    try:
                        specimen = Specimen.objects.filter(
                            specimen_label=luminex_result_row.specimen_label,
                            specimen_type=panel.specimen_type,
                            parent_label__isnull=False
                        ).first()
                        
                        if specimen is None:
                            specimen = Specimen.update_or_create_specimen_for_label(
                                luminex_result_row.specimen_label,
                                panel.specimen_type,
                                self.upload_file.specimen_label_type,
                                parent_label__isnull=False
                            )
                            if specimen.is_artificicial:
                                warning_msg += "Artificial aliquot created"
                        
                    except Specimen.DoesNotExist:
                         if luminex_result_row.specimen_purpose == "panel_specimen":
                             warning_msg += "Specimen not found\n"
                             specimen = None
                         else:
                             continue

                    luminex_result = LuminexCDCResult.objects.create(
                        specimen=specimen,
                        assay=assay,
                        laboratory=Laboratory.objects.get(name=luminex_result_row.laboratory),
                        test_date=datetime.strptime(luminex_result_row.test_date, '%Y-%m-%d').date(),
                        operator=luminex_result_row.operator,
                        assay_kit_lot=luminex_result_row.assay_kit_lot,
                        plate_identifier=luminex_result_row.plate_identifier,
                        test_mode=luminex_result_row.test_mode,
                        specimen_purpose=luminex_result_row.specimen_purpose,
                        specimen_label=luminex_result_row.specimen_label,
                        well_untreated=luminex_result_row.well_untreated,
                        well_treated=luminex_result_row.well_treated,
                        BSA_MFI=luminex_result_row.BSA_MFI or None,
                        IgG_MFI=luminex_result_row.IgG_MFI or None,
                        gp120_MFI=luminex_result_row.gp120_MFI or None,
                        gp160_MFI=luminex_result_row.gp160_MFI or None,
                        gp41_MFI=luminex_result_row.gp41_MFI or None,
                        BSA_MFImb=luminex_result_row.BSA_MFImb or None,
                        IgG_MFImb=luminex_result_row.IgG_MFImb or None,
                        gp120_MFImb=luminex_result_row.gp120_MFImb or None,
                        gp160_MFImb=luminex_result_row.gp160_MFImb or None,
                        gp41_MFImb=luminex_result_row.gp41_MFImb or None,
                        calibrator_BSA=luminex_result_row.calibrator_BSA or None,
                        calibrator_IgG=luminex_result_row.calibrator_IgG or None,
                        calibrator_gp120=luminex_result_row.calibrator_gp120 or None,
                        calibrator_gp160=luminex_result_row.calibrator_gp160 or None,
                        calibrator_gp41=luminex_result_row.calibrator_gp41 or None,
                        gp120_MFIn=luminex_result_row.gp120_MFIn or None,
                        gp160_MFIn=luminex_result_row.gp160_MFIn or None,
                        gp41_MFIn=luminex_result_row.gp41_MFIn or None,
                        DEA_treated_BSA_MFI=luminex_result_row.DEA_treated_BSA_MFI or None,
                        DEA_treated_IgG_MFI=luminex_result_row.DEA_treated_IgG_MFI or None,
                        DEA_treated_gp120_MFI=luminex_result_row.DEA_treated_gp120_MFI or None,
                        DEA_treated_gp160_MFI=luminex_result_row.DEA_treated_gp160_MFI or None,
                        DEA_treated_gp41_MFI=luminex_result_row.DEA_treated_gp41_MFI or None,
                        DEA_treated_BSA_MFImb=luminex_result_row.DEA_treated_BSA_MFImb or None,
                        DEA_treated_IgG_MFImb=luminex_result_row.DEA_treated_IgG_MFImb or None,
                        DEA_treated_gp120_MFImb=luminex_result_row.DEA_treated_gp120_MFImb or None,
                        DEA_treated_gp160_MFImb=luminex_result_row.DEA_treated_gp160_MFImb or None,
                        DEA_treated_gp41_MFImb=luminex_result_row.DEA_treated_gp41_MFImb or None,
                        DEA_treated_gp120_MFIn=luminex_result_row.DEA_treated_gp120_MFIn or None,
                        DEA_treated_gp160_MFIn=luminex_result_row.DEA_treated_gp160_MFIn or None,
                        DEA_treated_gp41_MFIn=luminex_result_row.DEA_treated_gp41_MFIn or None,
                        gp120_AI=luminex_result_row.gp120_AI or None,
                        gp160_AI=luminex_result_row.gp160_AI or None,
                        gp41_AI=luminex_result_row.gp41_AI or None,
                        warning_msg=warning_msg,
                        assay_run=assay_run
                    )

                    luminex_result = LuminexCDCResult.objects.get(pk=luminex_result.pk)
                    if luminex_result.specimen_purpose in ['kit_control','panel_specimen']:
                        # algorithms.do_curtis_alg2016(luminex_result)
                        algorithms.do_curtis_alg2013(luminex_result)

                    luminex_result_row.state = 'processed'
                    luminex_result_row.date_processed = timezone.now()
                    luminex_result_row.error_message = ''
                    luminex_result_row.luminex_result = luminex_result
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
