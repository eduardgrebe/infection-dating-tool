from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from cephia.models import Subject, SubjectEDDI, Visit, VisitEDDI
from diagnostics.models import DiagnosticTestHistory, TestPropertyEstimate
from datetime import timedelta
from django.db import transaction
from django.db.models import Q
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
                                                          result=lag_result.ODn)
            elif spec_results.count() > 1 and 'confirm' not in test_modes:
                import pdb; pdb.set_trace()
                summed_result = spec_results.aggregate(SUM('ODn'))

                #create result from mean of both records
            elif spec_results.count() > 1 and 'confirm' in test_modes:
                import pdb; pdb.set_trace()
                #create result from confirm3 record

    def _handle_lag_sedia(self, specimen_ids):
        pass
        #logic over here
