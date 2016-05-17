from django.core.management.base import BaseCommand, CommandError
import datetime
from cephia.models import Visit
from assay.models import PanelMemberships, Panel
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        try:
            panel = Panel.objects.get(pk=panel_id)
            assay_runs_for_panel = AssayRun.objects.filter(panel=panel)

            for run in assay_runs_for_panel:
                result_row_model = get_result_row_model(run.assay.name)
                rows_for_run = result_row_model.objects.filter(assay_run=assay_run)
                [ row.specimen_label for row in rows_for_run ]

            PanelMemberships.objects.create()

        except Exception, e:
            import pdb; pdb.set_trace()
        finally:
            error_file.close()
            the_file.close()
