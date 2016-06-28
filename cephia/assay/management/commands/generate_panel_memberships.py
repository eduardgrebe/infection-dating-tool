from django.core.management.base import BaseCommand, CommandError
import datetime
from cephia.models import Visit
from assay.models import PanelMembership, Panel, AssayRun, AssayResult
from assay import assay_result_factory
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Insert all panel memberships for existing panels'
    args = '<panel_id>'

    def handle(self, *args, **options):

        assay_run = AssayRun.objects.get(pk=args[0])
        
        results = AssayResult.objects.filter(assay_run__pk=args[0]).select_related('specimen', 'specimen__visit')

        visit_totals = defaultdict(lambda: 0)

        for result in results:
            visit = result.specimen.visit
            visit_totals[visit.pk] += 1

        for visit, visit_count in visit_totals.iteritems():
            PanelMembership.objects.create(
                visit_id=visit,
                replicates=visit_count,
                panel=assay_run.panel,
                category='',
                panel_inclusion_criterion=''
            )
                

