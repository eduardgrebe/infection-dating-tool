from django.core.management.base import BaseCommand, CommandError
from assay.models import (LagSediaResult, AssayRun, AssayResult, BioRadAvidityCDCResult,
                          BioRadAvidityJHUResult, ArchitectAvidityResult)
from django.db.models import Sum, Avg
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Calculate which results per run must move over to generic assay result table'
    args = '<run_id>'

    def handle(self, *args, **options):
        assay_run = AssayRun.objects.get(pk=args[0])
        assay = assay_run.assay.name

        if assay == 'LAg-Sedia':
            self._handle_lag_sedia(assay_run)
        elif assay == 'LAg-Maxim':
            self._handle_lag_maxim(assay_run)
        elif assay == 'ArchitectUnmodified':
            self._handle_architect_unmodified(assay_run)
        elif assay == 'ArchitectAvidity':
            self._handle_architect_avidity(assay_run)
        elif assay == 'BioRadAvidity-CDC':
            self._handle_biorad_avidity_cdc(assay_run)
        elif assay == 'BioRadAvidity-JHU':
            self._handle_biorad_avidity_jhu(assay_run)
        elif assay == 'Vitros':
            self._handle_vitros_avidity(assay_run)
        elif assay == 'LSVitros-Diluent':
            self._handle_ls_vitros_diluent(assay_run)
        elif assay == 'LSVitros-Plasma':
            self._handle_ls_vitros_plasma(assay_run)
        elif assay == 'Geenius':
            self._handle_geenius(assay_run)
        elif assay == 'BED':
            self._handle_BED(assay_run)
        elif assay == 'BioRadAvidity-Glasgow':
            self._handle_biorad_avidity_glasgow(assay_run)
        elif assay == 'BioPlex-CDC':
            self._handle_bioplex_cdc(assay_run)
        elif assay == 'BioPlex-Duke':
            self._handle_bioplex_duke(assay_run)
        elif assay == 'IDE-iV3':
            self._handle_idev3(assay_run)
        elif assay == '':
            self._handle_immunetics_mixl(assay_run)
        elif assay == '':
            self._handle_immunetics_newmix(assay_run)
        elif assay == '':
            self._handle_immunetics_newmixpeptide(assay_run)

    def _handle_lag_sedia(self, assay_run):
        specimen_ids = LagSediaResult.objects.values_list('specimen', flat=True).filter(assay_run=assay_run).distinct()
        for specimen_id in specimen_ids:
            spec_results = LagSediaResult.objects.filter(assay_run=assay_run, specimen__id=specimen_id)
            test_modes = [ spec.test_mode for spec in spec_results ]
            lag_result = spec_results[0]

            if spec_results.count() == 1:
                final_result = lag_result.ODn
                method = 'singlet'
            elif spec_results.count() > 1 and 'confirm_3' not in test_modes:
                final_result = spec_results.aggregate(Sum('ODn'))['ODn__sum'] / spec_results.count()
                method = 'mean_ODn_screen'
            elif spec_results.count() > 1 and 'confirm_3' in test_modes:
                confirm_results = sorted([ result.ODn for result in spec_results.filter(test_mode__startswith='confirm') ])
                final_result = confirm_results[1]
                method = 'median_of_confirms'

            assay_result = AssayResult.objects.create(panel=assay_run.panel,
                                                      assay=assay_run.assay,
                                                      specimen=lag_result.specimen,
                                                      assay_run=assay_run,
                                                      test_date=lag_result.test_date,
                                                      method=method,
                                                      result=final_result)

    def _handle_lag_maxim(self, assay_run):
        pass

    def _handle_architect_unmodified(self, assay_run):
        pass

    def _handle_architect_avidity(self, assay_run):
        warning_msg = ''
        specimen_ids = ArchitectAvidityResult.objects.values_list('specimen', flat=True)\
                                                     .filter(assay_run=assay_run)\
                                                     .exclude(test_mode='control').distinct()

        with transaction.atomic():
            for specimen_id in specimen_ids:
                spec_results = ArchitectAvidityResult.objects.filter(assay_run=assay_run, specimen__id=specimen_id)
                test_modes = [ spec.test_mode for spec in spec_results ]
                number_of_confirms = len([mode for mode in test_modes if "conf" in mode])
                number_of_screens = len([mode for mode in test_modes if "screen" in mode])
                architect_result = spec_results[0]

                if spec_results.count() == 1:
                    final_result = architect_result.AI
                    method = 'singlet'
                elif number_of_screens > 1 and number_of_confirms == 0:
                    spec_result = spec_results.filter(test_mode__startswith='screen')
                    untreated_mean = spec_results.aggregate(Sum('untreated_pbs_SCO'))['untreated_pbs_SCO__sum'] / spec_results.count()
                    treated_mean = spec_results.aggregate(Sum('treated_guanidine_SCO'))['treated_guanidine_SCO__sum'] / spec_results.count()
                    final_result = treated_mean / untreated_mean * 100
                    method = 'mean_SCO_treated/mean_SCO_untreated*100'
                    warning_msg += 'More than 1 screen result.'
                elif number_of_confirms > 0:
                    spec_result = spec_results.filter(test_mode__startswith='confirm')
                    untreated_mean = spec_results.aggregate(Sum('untreated_pbs_SCO'))['untreated_pbs_SCO__sum'] / spec_results.count()
                    treated_mean = spec_results.aggregate(Sum('treated_guanidine_SCO'))['treated_guanidine_SCO__sum'] / spec_results.count()
                    final_result = treated_mean / untreated_mean * 100
                    method = 'mean_SCO_treated/mean_SCO_untreated*100'

                if number_of_confirms != 2:
                    warning_msg += "Unexpected number of 'confirm' records."
                if number_of_screens == 0:
                    warning_msg += "\nNo 'screen' records."

                assay_result = AssayResult.objects.create(panel=assay_run.panel,
                                                          assay=assay_run.assay,
                                                          specimen=architect_result.specimen,
                                                          assay_run=assay_run,
                                                          test_date=architect_result.test_date,
                                                          method=method,
                                                          result=final_result,
                                                          warning_msg=warning_msg)

    def _handle_biorad_avidity_cdc(self, assay_run):
        warning_msg = ''
        specimen_ids = BioRadAvidityCDCResult.objects.values_list('specimen', flat=True) \
                                                     .filter(assay_run=assay_run) \
                                                     .exclude(test_mode='control').distinct()

        with transaction.atomic():
            for specimen_id in specimen_ids:
                spec_results = BioRadAvidityCDCResult.objects.filter(assay_run=assay_run, specimen__id=specimen_id)
                test_modes = [ spec.test_mode for spec in spec_results ]
                biorad_result = spec_results[0]
                number_of_confirms = len([mode for mode in test_modes if "conf" in mode])
                number_of_screens = len([mode for mode in test_modes if "screen" in mode])
                if spec_results.count() == 1:
                    final_result = biorad_result.AI
                    method = 'singlet'
                elif spec_results.count() > 1 and number_of_confirms == 0:
                    spec_results = spec_results.filter(test_mode__startswith='screen')
                    final_result = spec_results.aggregate(Sum('AI'))['AI__sum'] / spec_results.count()
                    warning_msg += 'More than 1 screen result.'
                    method = 'mean_of_screen_AIs'
                elif spec_results.count() > 1 and number_of_confirms > 0:
                    spec_results = spec_results.filter(test_mode__startswith='confirm')
                    final_result = spec_results.aggregate(Sum('AI'))['AI__sum'] / spec_results.count()
                    method = 'mean_of_confirm_AIs'

                if number_of_confirms != 2:
                    warning_msg += "Unexpected number of 'confirm' records."
                if number_of_screens == 0:
                    warning_msg += "\nNo 'screen' records."

                assay_result = AssayResult.objects.create(panel=assay_run.panel,
                                                          assay=assay_run.assay,
                                                          specimen=biorad_result.specimen,
                                                          assay_run=assay_run,
                                                          test_date=biorad_result.test_date,
                                                          method=method,
                                                          result=final_result,
                                                          warning_msg=warning_msg)

    def _handle_biorad_avidity_jhu(self, assay_run):
        pass

    def _handle_vitros_avidity(self, assay_run, specimen_ids):
        warning_msg = ''

        specimen_ids = VitrosAvidityResult.objects.values_list('specimen', flat=True).filter(assay_run=assay_run).exclude(test_mode='control').distinct()

        for specimen_id in specimen_ids:
            spec_results = VitrosAvidityResult.objects.filter(assay_run=assay_run, specimen__id=specimen_id)
            test_modes = [ spec.test_mode for spec in spec_results ]
            number_of_screens = len([mode for mode in test_modes if "screen" in mode])
            number_of_confirms = len([mode for mode in test_modes if "confirm" in mode])
            vitros_result = spec_results[0]

            final_result = spec_results.aggregate(Sum('AI'))['AI__sum'] / spec_results.count()
            if spec_results.count() == 1:
                method = 'singlet'
            elif spec_results.count() > 1:
                method = 'mean_of_AIs'
                warning_msg = 'Unexpected number of results.'

            if number_of_confirms > 0:
                warning_msg += "Unexpected 'confirm' records."
            if number_of_screens == 0:
                warning_msg += "\nNo 'screen' records."

            assay_result = AssayResult.objects.create(panel=assay_run.panel,
                                                      assay=assay_run.assay,
                                                      specimen=biorad_result.specimen,
                                                      assay_run=assay_run,
                                                      test_date=biorad_result.test_date,
                                                      method=method,
                                                      result=final_result,
                                                      warning_msg=warning_msg)

    def _handle_ls_vitros_diluent(self, assay_run, specimen_ids):
        warning_msg = ''

        specimen_ids = LSVitrosDiluentResult.objects.values_list('specimen', flat=True).filter(assay_run=assay_run).exclude(test_mode='control').distinct()

        for specimen_id in specimen_ids:
            with transaction.atomic():
                spec_results = LSVitrosDiluentResult.objects.filter(assay_run=assay_run, specimen__id=specimen_id)
                test_modes = [ spec.test_mode for spec in spec_results ]
                ls_vitros_result = spec_results[0]
                number_of_screens = len([mode for mode in test_modes if "screen" in mode])
                number_of_confirms = len([mode for mode in test_modes if "conf" in mode])

                if spec_results.count() == 1:
                    final_result = ls_vitros_result.SCO
                    method = 'singlet'
                elif number_of_screens > 0 and number_of_confirms == 0:
                    spec_results = spec_results.filter(test_mode__startswith='screen')
                    final_result = spec_results.aggregate(Sum('SCO'))['SCO__sum'] / spec_results.count()
                    method = 'mean_of_screen_SCOs'
                elif number_of_confirms > 0:
                    spec_results = spec_results.filter(test_mode__startswith='confirm')
                    final_result = spec_results.aggregate(Sum('SCO'))['SCO__sum'] / spec_results.count()
                    method = 'mean_of_confirm_SCOs'

                if number_of_confirms > 0 and number_of_confirms != 2:
                    warning_msg += "Unexpected number of 'confirm' records."
                if number_of_screens == 0:
                    warning_msg += "\nNo 'screen' records."

                    assay_result = AssayResult.objects.create(panel=assay_run.panel,
                                                              assay=assay_run.assay,
                                                              specimen=ls_vitros_result.specimen,
                                                              assay_run=assay_run,
                                                              test_date=ls_vitros_result.test_date,
                                                              method=method,
                                                              result=final_result,
                                                              warning_msg=warning_msg)

    def _handle_ls_vitros_plasma(self, assay_run, specimen_ids):
        specimen_ids = LSVitrosPlasmaResult.objects.values_list('specimen', flat=True).filter(assay_run=assay_run).exclude(test_mode='control').distinct()

        for specimen_id in specimen_ids:
            with transaction.atomic():
                spec_results = LSVitrosPlasmaResult.objects.filter(assay_run=assay_run, specimen__id=specimen_id)
                test_modes = [ spec.test_mode for spec in spec_results ]
                ls_vitros_result = spec_results[0]
                number_of_screens = len([mode for mode in test_modes if "screen" in mode])
                number_of_confirms = len([mode for mode in test_modes if "conf" in mode])

                if spec_results.count() == 1:
                    final_result = ls_vitros_result.SCO
                    method = 'singlet'
                elif number_of_screens > 0 and number_of_confirms == 0:
                    spec_results = spec_results.filter(test_mode__startswith='screen')
                    final_result = spec_results.aggregate(Sum('SCO'))['SCO__sum'] / spec_results.count()
                    method = 'mean_of_screen_SCOs'
                elif number_of_confirms > 0:
                    spec_results = spec_results.filter(test_mode__startswith='confirm')
                    final_result = spec_results.aggregate(Sum('SCO'))['SCO__sum'] / spec_results.count()
                    method = 'mean_of_confirm_SCOs'

                if number_of_confirms > 0 and number_of_confirms != 2:
                    warning_msg += "Unexpected number of 'confirm' records."
                if number_of_screens == 0:
                    warning_msg += "\nNo 'screen' records."

                    assay_result = AssayResult.objects.create(panel=assay_run.panel,
                                                              assay=assay_run.assay,
                                                              specimen=ls_vitros_result.specimen,
                                                              assay_run=assay_run,
                                                              test_date=ls_vitros_result.test_date,
                                                              method=method,
                                                              result=final_result,
                                                              warning_msg=warning_msg)

    def _handle_geenius(self, assay_run, specimen_ids):
        pass

    def _handle_BED(self, assay_run, specimen_ids):
        specimen_ids = BEDResult.objects.values_list('specimen', flat=True).filter(assay_run=assay_run).distinct()
        for specimen_id in specimen_ids:
            spec_results = BEDResult.objects.filter(assay_run=assay_run, specimen__id=specimen_id)
            test_modes = [ spec.test_mode for spec in spec_results ]
            bed_result = spec_results[0]

            if spec_results.count() == 1:
                final_result = bed_result.ODn
                method = 'singlet'
            elif spec_results.count() > 1 and 'confirm_3' not in test_modes:
                final_result = spec_results.aggregate(Sum('ODn'))['ODn__sum'] / spec_results.count()
                method = 'mean_ODn_screen'
            elif spec_results.count() > 1 and 'confirm_3' in test_modes:
                confirm_results = sorted([ result.ODn for result in spec_results.filter(test_mode__startswith='confirm') ])
                final_result = confirm_results[1]
                method = 'median_of_confirms'

            assay_result = AssayResult.objects.create(panel=assay_run.panel,
                                                      assay=assay_run.assay,
                                                      specimen=bed_result.specimen,
                                                      assay_run=assay_run,
                                                      test_date=bed_result.test_date,
                                                      method=method,
                                                      result=final_result)

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

