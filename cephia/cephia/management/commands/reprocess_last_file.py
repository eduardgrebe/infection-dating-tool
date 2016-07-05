from django.core.management.base import BaseCommand, CommandError
import datetime
from cephia.models import FileInfo, Laboratory
from assay.models import AssayResult, BaseAssayResult, AssayRun
import logging
from django.utils import timezone
from django.core.management import call_command
from assay.assay_result_factory import *

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Reprocesses the latest file info object'

    def handle(self, *args, **options):
        result_file = FileInfo.objects.last()
        result_file.message = ''
        result_file.save()
        run = AssayRun.objects.filter(fileinfo=result_file).first()

        if run:
            AssayResult.objects.filter(assay_run=run).delete()
            get_result_model(run.assay.name).objects.filter(assay_run=run).delete()
            get_result_row_model(run.assay.name).objects.filter(fileinfo=result_file).delete()
            run.delete()
            
        result_file.get_handler().parse()
        result_file.get_handler().validate(result_file.panel.id)

        assay_run = AssayRun.objects.create(
            panel=result_file.panel,
            assay=result_file.assay,
            laboratory=Laboratory.objects.last(),
            fileinfo=result_file,
            run_date=timezone.now())
        
        result_file.get_handler().process(result_file.panel.id, assay_run)
        call_command('assay_results_per_run', str(assay_run.id))
