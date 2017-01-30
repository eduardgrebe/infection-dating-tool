from django.core.management.base import BaseCommand, CommandError
from outside_eddi.models import OutsideEddiDiagnosticTest, OutsideEddiTestPropertyEstimate
from outside_eddi.file_handlers.outside_eddi_test_and_properties_file_handler import TestsAndPropertiesFileHandler
from django.db.models import F
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update or create global tests and test properties for the Cephia Infection Dating Tool'

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR
        uploaded_file = open("%s/outside_eddi/static/test_and_properties/DiagnosticTests_and_Properties.csv" %base_dir, "rb")
        TestsAndPropertiesFileHandler(uploaded_file).import_data()

