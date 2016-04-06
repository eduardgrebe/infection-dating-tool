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

    def _handle_lag_sedia(self, specimen_ids):
        pass
