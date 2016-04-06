from django.core.management.base import BaseCommand, CommandError
from assay.models import LagSediaResult, AssayRun, AssayResult
from django.db.models import Sum
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Calculate which results per run must move over to generic assay result table'
    args = '<run_id>'

    def handle(self, *args, **options):
        assay_run = AssayRun.objects.get(pk=args[0])
        assay = assay_run.assay.short_name
        
        if assay = 'LAg-Sedia':
            self._handle_lag_sedia(assay_run)

        elif assay = 'LAg-Maxim':
            self._handle_lag_maxim(assay_run)
        
        elif assay = 'ArchitectUnmodified':
            self._handle_architect_unmodified(assay_run, specimen_ids)

        elif assay = 'ArchitectAvidity':
            self._handle_architect_avidity(assay_run, specimen_ids)

        elif assay = 'BioRadAvidity-CDC':
            self._handle_biorad_avidity_cdc(assay_run, specimen_ids)

        elif assay = '':
            self._handle_biorad_avidity_jhu(assay_run, specimen_ids)

        elif assay = '':
            self._handle_vitros_avidity(assay_run, specimen_ids)

        elif assay = '':
            self._handle_ls_vitros_diluent(assay_run, specimen_ids)

        elif assay = '':
            self._handle_ls_vitros_plasma(assay_run, specimen_ids)

        elif assay = '':
            self._handle_geenius(assay_run, specimen_ids)

        elif assay = '':
            self._handle_BED(assay_run, specimen_ids)

        elif assay = '':
            self._handle_biorad_avidity_glasgow(assay_run, specimen_ids)

        elif assay = '':
            self._handle_bioplex_cdc(assay_run, specimen_ids)

        elif assay = '':
            self._handle_bioplex_duke(assay_run, specimen_ids)

        elif assay = '':
            self._handle_idev3(assay_run, specimen_ids)

        elif assay = '':
            self._handle_bioplex_duke(assay_run, specimen_ids)

        elif assay = '':
            self._handle_immunetics_mixl(assay_run, specimen_ids)

        elif assay = '':
            self._handle_immunetics_newmix(assay_run, specimen_ids)

        elif assay = '':
            self._handle_immunetics_newmixpeptide(assay_run, specimen_ids)

    def _handle_lag_sedia(self, assay_run, specimen_ids):
        specimen_ids = LagSediaResult.objects.values_list('specimen', flat=True).filter(assay_run=assay_run)
         for specimen_id in specimen_ids:
            spec_results = LagSediaResult.objects.filter(assay_run=assay_run, specimen__id=specimen_id)
            test_modes = [ spec.test_mode for spec in spec_results ]
            lag_result = spec_results[0]

            if spec_results.count() == 1:
                final_result = lag_result.ODn
            elif spec_results.count() > 1 and 'confirm' not in test_modes:
                final_result = spec_results.aggregate(Sum('ODn'))['ODn__sum'] / spec_results.count()
            elif spec_results.count() > 1 and 'confirm' in test_modes:
                final_result = spec_results.get(test_mode='confirm_3').ODn

            assay_result = AssayResult.objects.create(panel=assay_run.panel,
                                                      assay=assay_run.assay,
                                                      specimen=lag_result.specimen,
                                                      assay_run=assay_run,
                                                      test_date=lag_result.test_date,
                                                      result=final_result)

    def _handle_lag_maxim(self, assay_run, specimen_ids):
        pass

    def _handle_architect_unmodified(self, assay_run, specimen_ids):
        pass

    def _handle_architect_avidity(self, assay_run, specimen_ids):
        pass

    def _handle_biorad_avidity_cdc(self, assay_run, specimen_ids):
        specimen_ids = LagSediaResult.objects.values_list('specimen', flat=True).filter(assay_run=assay_run)
        for specimen_id in specimen_ids:
            spec_results = LagSediaResult.objects.filter(assay_run=assay_run, specimen__id=specimen_id)
            test_modes = [ spec.test_mode for spec in spec_results ]:
            if spec_results.count() == 1:
                lag_result = spec_results[0]
                assay_result = AssayResult.objects.create(panel=lag_result.panel,
                                                          assay=lag_result.assay,
                                                          specimen=lag_result.specimen,
                                                          assay_run=assay_run,
                                                          test_date=lag_result.test_date,
                                                          result=lag_result.result_AI)
            elif spec_results.count() > 1 and 'confirm' not in test_modes:
                # take treated ODs and get mean
                # divide result by the mean of the untreated ODs
                # in other words mean of treated / mean of untreated

                lag_result = spec_results[0]
                assay_result = AssayResult.objects.create(panel=lag_result.panel,
                                                          assay=lag_result.assay,
                                                          specimen=lag_result.specimen,
                                                          assay_run=assay_run,
                                                          test_date=lag_result.test_date,
                                                          result=result)
            elif spec_results.count() > 1 and 'confirm' in test_modes:
                lag_result = spec_results.get(test_mode='confirm_3')
                assay_result = AssayResult.objects.create(panel=lag_result.panel,
                                                          assay=lag_result.assay,
                                                          specimen=lag_result.specimen,
                                                          assay_run=assay_run,
                                                          test_date=lag_result.test_date,
                                                          result=lag_result.result_AI)

        pass

    def _handle_biorad_avidity_jhu(self, assay_run, specimen_ids):
        pass

    def _handle_vitros_avidity(self, assay_run, specimen_ids):
        pass

    def _handle_ls_vitros_diluent(self, assay_run, specimen_ids):
        pass

    def _handle_ls_vitros_plasma(self, assay_run, specimen_ids):
        pass

    def _handle_geenius(self, assay_run, specimen_ids):
        pass

    def _handle_BED(self, assay_run, specimen_ids):
        pass

    def _handle_idev3_handle_biorad_avidity_glasgow(self, assay_run, specimen_ids):
        pass

    def _handle_bioplex_cdc(self, assay_run, specimen_ids):
        pass

    def _handle_bioplex_duke(self, assay_run, specimen_ids):
        pass

    def _handle_idev3(self, assay_run, specimen_ids):
        pass

    def _handle_immunetics_mixl(self, assay_run, specimen_ids):
        pass

    def _handle_immunetics_newmix(self, assay_run, specimen_ids):
        pass

    def _handle_immunetics_newmixpeptide(self, assay_run, specimen_ids):
        pass

