from celery import task
from cephia.models import FileInfo, Laboratory
from django.utils import timezone
from django.core.management import call_command

from assay.models import AssayRun
from lib import log_exception

@task
def process_file_info(pk, lab_id):
    result_file = FileInfo.objects.get(pk=pk)
    result_file.task_id = process_file_info.request.id
    result_file.save()

    try:
        result_file.get_handler().parse()
        result_file.get_handler().validate(result_file.panel.id)

        assay_run = AssayRun.objects.create(
            panel=result_file.panel,
            assay=result_file.assay,
            laboratory=Laboratory.objects.filter(pk=lab_id).first(),
            fileinfo=result_file,
            run_date=timezone.now())

        result_file.get_handler().process(result_file.panel.id, assay_run)
        call_command('assay_results_per_run', str(assay_run.id))
        assay_run.check_replicate_counts()
    except Exception, e:
        result_file.message = 'Could not process file: ' + log_exception(e)
        result_file.state = 'error'
        result_file.save()
        
    finally:
        FileInfo.objects.filter(pk=pk).update(task_id=None)
