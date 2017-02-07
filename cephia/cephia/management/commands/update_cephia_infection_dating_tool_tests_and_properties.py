from django.core.management.base import BaseCommand, CommandError
from infection_dating_tool.models import IDTDiagnosticTest, IDTTestPropertyEstimate
from infection_dating_tool.file_handlers.idt_test_and_properties_file_handler import TestsAndPropertiesFileHandler
from django.db.models import F
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update or create global tests and test properties for the Cephia Infection Dating Tool'

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR
        print base_dir
        uploaded_file = open("%s/infection_dating_tool/static/test_and_properties/Diagnostic Tests and Properties Public.csv" %base_dir, "rb")
        TestsAndPropertiesFileHandler(uploaded_file).import_data()

