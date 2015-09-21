from django.core.management.base import BaseCommand, CommandError
from cephia.models import FileInfo
import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import files in status - pending'

    def handle(self, *args, **options):
        for file_to_import in FileInfo.objects.filter(state='pending'):
            try:
                file_handler = file_to_import.get_handler()
                msg = file_handler.validate_file()

                if msg:
                    file_to_import.message = msg

                num_success, num_fail = file_handler.parse()

                fail_msg = 'Failed to import %s rows ' % str(num_fail)
                msg = 'Successfully imported %s rows ' % str(num_success)
            
                if num_fail > 0:
                    file_to_import.state = 'row_error'
                else:
                    file_to_import.state = 'imported'

                file_to_import.message += '\n%s.\n%s' % (fail_msg, msg)
                file_to_import.save()

                logger.info('Successfully imported file "%s"' % file_to_import)
            except Exception, e:
                logger.exception(e)
                file_to_import.state = 'file_error'
                file_to_import.message = 'Import failed: ' + e.message
                file_to_import.save()
                continue
