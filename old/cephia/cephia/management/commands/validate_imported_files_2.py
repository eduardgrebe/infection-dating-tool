from django.core.management.base import BaseCommand, CommandError
from cephia.models import FileInfo
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):

    help = 'Validate aliquot and transfer out files in status - imported'

    def handle(self, *args, **options):
        for file_to_validate in FileInfo.objects.filter(state='imported', priority__in=[4,5, 6]).order_by('priority'):
            try:
                file_handler = file_to_validate.get_handler()

                num_success, num_fail = file_handler.validate()

                fail_msg = 'Failed to validate %s rows ' % str(num_fail)
                msg = 'Successfully validated %s rows ' % str(num_success)

                if num_fail > 0:
                    file_to_validate.state = 'row_error'
                else:
                    file_to_validate.state = 'validated'

                file_to_validate.message += '\n%s.\n%s' % (fail_msg, msg)
                file_to_validate.save()
            except Exception, e:
                logger.exception(e)
                file_to_validate.state = 'file_error'
                file_to_validate.message = e.message
                file_to_validate.save()

            logger.info('Successfully validated file "%s"' % file_to_validate)
