from django.core.management.base import BaseCommand, CommandError
import datetime
from cephia.models import Visit
from assay.models import PanelMemberships, Panel, AssayRun
from assay import assay_result_factory
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Insert all panel memberships for existing panels'
    args = '<panel_id>'

    def handle(self, *args, **options):
        try:
            panel = Panel.objects.get(pk=args[0])
            assay_runs_for_panel = AssayRun.objects.filter(panel=panel)
            visits_for_run= []

            for run in assay_runs_for_panel:
                result_model = get_result_model(run.assay.name)
                rows_for_run = result_model.objects.filter(assay_run=run)
                visits_for_run = list(set(visits_for_run) | set([ row.specimen.visit for row in rows_for_run ]))

            import pdb; pdb.set_trace()
            #PanelMemberships.objects.create()
        except Exception, e:
            import pdb; pdb.set_trace()
