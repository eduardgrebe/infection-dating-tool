from django.core.management.base import BaseCommand, CommandError
from cephia.models import FileInfo
import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Process files in status - validated'

    def handle(self, *args, **options):
        for file_to_process in FileInfo.objects.filter(state__in=['validated','row_error']).order_by('priority'):
            try:
                file_handler = file_to_process.get_handler()
        
                num_success, num_fail = file_handler.process()

                fail_msg = 'Failed to process %s rows ' % str(num_fail)
                msg = 'Successfully processed %s rows ' % str(num_success)

                if num_fail > 0:
                    file_to_process.state = 'row_error'
                else:
                    file_to_process.state = 'processed'
                    
                file_to_process.message += '\n%s.\n%s' % (fail_msg, msg)
                file_to_process.save()
            except Exception, e:
                logger.exception(e)
                file_to_process.state = 'file_error'
                file_to_process.message = 'Failed to process: ' + e.message
                file_to_process.save()
                continue

            logger.info('Successfully processed file "%s"' % file_to_process)
