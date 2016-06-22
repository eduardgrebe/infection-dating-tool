from assay.models import BioRadAvidityGlasgowResult, AssayResult
from django.db.models import Sum, Q
from django.db import transaction
# from lib import log_exception

class BioRadCalculation(object):

    def __init__(self, assay_run, result_class=None, treatment_columns = None):

        treatment_columns = treatment_columns or ['treated_urea_OD', 'untreated_buffer_OD']
        self._treated_column = treatment_columns[0]
        self._untreated_column = treatment_columns[1]
        self.assay_run = assay_run
        self.result_class = result_class or BioRadAvidityGlasgowResult
        self.specimen_ids = self.result_class.objects.values_list('specimen', flat=True)\
                                                              .filter(assay_run=self.assay_run)\
                                                              .exclude(test_mode='control').distinct()

    def screen_only(self):
        method = None
        warning_msg = []
        final_result = None
        
        if self.number_of_valid_screens == 1:
            final_result = self.valid_results[0].AI
            method = 'sop_screen_singlet'
            
            if self.first_result.AI >= 30 and self.first_result.AI <= 50:
                warning_msg.append('Greyzone AI - Confirms absent.')
                
            if self.first_result.untreated_buffer_OD < 1:
                warning_msg.append('Retests absent. buffer_OD < 1')
            elif self.first_result.untreated_buffer_OD > 4 and self.first_result.treated_urea_OD < 3.5:
                warning_msg.append('Retests absent. buffer_OD > 4 and urea_OD < 3.5')
        elif self.number_of_valid_screens > 1:
            warning_msg += 'Unexpected number of screens. Found %s.\n' % self.number_of_valid_screens
            final_result = None
        else:
            final_result = None
            warning_msg.append("All screen records excluded.")

        return final_result, method, ''.join(warning_msg)

    def screen_and_retest_only(self):
        method = None
        warning_msg = []
        final_result = None

        if self.number_of_valid_retests == 1:
            final_result = self.valid_results.filter(test_mode__endswith='_retest')[0].AI
            
            if final_result >= 30 and final_result <= 50:
                warning_msg.append('Greyzone AI - Confirms absent.')

            if self.total_screens == 0:
                warning_msg.append('Retests, but no screen records.')
            
            method = 'sop_retest_singlet'
        elif self.number_of_valid_retests > 1:
            warning_msg.append("More than 1 non-excluded retest. Found %s\n" % self.number_of_valid_retests)
            final_result = None
        elif self.number_of_valid_retests == 0 and self.number_of_valid_screens > 0:
            final_result, method, warning_msg = self.screen_only()

        return final_result, method, ''.join(warning_msg)

    def screen_and_conf_only(self):
        method = None
        warning_msg = ''
        final_result = None

        if self.number_of_valid_confirms == 0 or self.number_of_valid_screens == 0:
            final_result, method, warning_msg = self.screen_only()
        elif self.number_of_valid_screens == 1 and self.number_of_valid_confirms == 2:
            final_result = self.valid_results.aggregate(Sum('AI'))['AI__sum'] / 3
            method = 'sop_mean_screen_confirms'
        elif self.number_of_valid_screens > 1:
            final_result = None
            warning_msg += 'Unexpected number of screens. Found %s.\n' % self.number_of_valid_screens
        elif self.number_of_valid_confirms != 2:
            final_result = None
            warning_msg += 'Unexpected number of confirms. Found %s.\n' % self.number_of_valid_confirms

        return final_result, method, warning_msg

    def screen_retest_conf(self):
        method = None
        warning_msg = ''
        final_result = None

        if self.number_of_valid_retests == 0 and self.number_of_valid_confirms > 0:
            final_result, method, warning_msg = self.screen_and_conf_only()
        elif self.number_of_valid_confirms == 0:
            final_result, method, warning_msg = self.screen_and_retest_only()
        elif self.number_of_valid_retests > 1:
            warning_msg += 'Unexpected number of retests. Found %s.\n' % self.number_of_valid_retests
        elif self.number_of_valid_confirms != 2:
            warning_msg += 'Unexpected number of confirms. Found %s.\n' % self.number_of_valid_confirms
        elif self.number_of_valid_retests == 1 and self.number_of_valid_confirms == 2:
            final_result = self.valid_results.filter(Q(test_mode__endswith='_retest') | Q(test_mode__startswith='confirm'))\
                                             .aggregate(Sum('AI'))['AI__sum'] / 3
            method = 'sop_mean_retest_confirms'
        else:
            warning_msg += 'Unexpected number of records.\n'

        return final_result, method, warning_msg

    def calculate(self):
        with transaction.atomic():
            for specimen_id in self.specimen_ids:
                try:
                    self.spec_results = self.result_class.objects.filter(assay_run=self.assay_run, specimen__id=specimen_id)

                    self.spec_results.update(assay_result=None)
                    AssayResult.objects.filter(assay_run=self.assay_run, specimen__id=specimen_id).delete()


                    self.valid_results = BioRadAvidityGlasgowResult.objects.filter(
                        assay_run=self.assay_run, specimen__id=specimen_id)\
                                                                           .exclude(exclusion='1')
                    self.valid_result_count = self.valid_results.count()
                    self.valid_test_modes = [ spec.test_mode for spec in self.valid_results ]
                    self.number_of_valid_retests = len([mode for mode in self.valid_test_modes if mode.endswith("_retest") ])
                    self.number_of_valid_screens = len([mode for mode in self.valid_test_modes if mode.startswith('screen')\
                                                        and not mode.endswith('_retest') ])
                    self.number_of_valid_confirms = len([ mode for mode in self.valid_test_modes if "confirm" in mode ])
                    self.invalid_results = self.result_class.objects.filter(assay_run=self.assay_run, specimen__id=specimen_id)\
                                                                             .exclude(exclusion='0')
                    self.invalid_result_count = self.invalid_results.count()
                    self.invalid_test_modes = [ spec.test_mode for spec in self.spec_results ]
                    self.number_of_invalid_retests = len([mode for mode in self.invalid_test_modes if "_retest" in mode])
                    self.number_of_invalid_screens = len([mode for mode in self.invalid_test_modes if mode.startswith('screen')\
                                                          and not mode.endswith('_retest') ])
                    self.number_of_invalid_confirms = len([mode for mode in self.invalid_test_modes if "confirm" in mode])
                    self.total_screens = self.number_of_valid_screens + self.number_of_invalid_screens
                    self.total_retests = self.number_of_valid_retests + self.number_of_invalid_retests
                    self.total_confirms = self.number_of_valid_confirms + self.number_of_invalid_confirms

                    if self.valid_result_count == 0:
                        raise Exception("No valid results on specimen")
                    else:
                        self.first_result = self.valid_results[0]

                    if self.total_screens > 0 and self.total_retests == 0 and self.total_confirms == 0:
                        final_result, method, warning_msg = self.screen_only()
                    elif self.total_retests > 0 and self.total_confirms == 0:
                        final_result, method, warning_msg = self.screen_and_retest_only()
                    elif self.total_retests == 0 and self.total_screens > 0 and self.total_confirms > 0:
                        final_result, method, warning_msg = self.screen_and_conf_only()
                    elif self.total_retests > 0 and self.total_confirms > 0:
                        final_result, method, warning_msg = self.screen_retest_conf()
                    else:
                        method = None
                        final_result = None
                        warning_msg = "Unhandled scenario!"

                    assay_result = AssayResult.objects.create(
                        panel=self.assay_run.panel,
                        assay=self.assay_run.assay,
                        specimen=self.first_result.specimen,
                        assay_run=self.assay_run,
                        test_date=self.first_result.test_date,
                        method=method,
                        result=final_result,
                        warning_msg=warning_msg)
                    self.spec_results.update(assay_result=assay_result)
                except Exception, e:
                    method = None
                    final_result = None
                    warning_msg = e.message

                    assay_result = AssayResult.objects.create(
                        panel=self.assay_run.panel,
                        assay=self.assay_run.assay,
                        specimen=self.spec_results[0].specimen,
                        assay_run=self.assay_run,
                        test_date=self.spec_results[0].test_date,
                        method=method,
                        result=final_result,
                        warning_msg=warning_msg)
                    self.spec_results.update(assay_result=assay_result)
                    continue

