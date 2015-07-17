from django.core.management.base import BaseCommand, CommandError
from cephia.models import FileInfo
import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Process files in status - pending'

    def handle(self, *args, **options):

        for file_to_process in FileInfo.objects.filter(state='imported'):
            try:
                file_handler = file_to_process.get_handler()
        
                num_success, num_fail = file_handler.process()

                fail_msg = 'Failed to process ' + str(num_fail) + ' rows '
                msg = 'Successfully processed ' + str(num_success) + ' rows '

                if num_fail > 0:
                    file_to_process.state = 'error'
                else:
                    file_to_process.state = 'processed'
            
                file_to_process.message = fail_msg + ' ' + msg
                file_to_process.save()
            except Exception, e:
                logger.exception(e)
                file_to_process.state = 'error'
                file_to_process.message = 'Failed to process: ' + e.message
                file_to_process.save()
                continue

            logger.info('Successfully processed file "%s"' % file_to_process)
