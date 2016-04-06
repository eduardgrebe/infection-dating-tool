from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from cephia.models import Subject, SubjectEDDI, Visit, VisitEDDI
from diagnostics.models import DiagnosticTestHistory, TestPropertyEstimate
from datetime import timedelta
from django.db import transaction
from django.db.models import Q
rom django.db.models import Sum
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Calculate which results per run must move over to generic assay result table'

    def handle(self, *args, **options):
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

    def _handle_lag_sedia(self, specimen_ids):
        pass
