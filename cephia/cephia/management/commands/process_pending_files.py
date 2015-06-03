from django.core.management.base import BaseCommand, CommandError
from cephia.models import FileInfo
import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Process files in status - pending'

    def handle(self, *args, **options):

        for file_info in FileInfo.objects.filter(state='pending'):

            #handle file parsing over here based on file type

            file_info.state = 'imported'
            file_info.save()

            logger.info('Successfully processed file "%s"' % file_info)
