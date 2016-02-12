from django.core.management.base import BaseCommand, CommandError
from diagnostics.models import DiagnosticTestHistory
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update all adjusted dates for testing history'

    def handle(self, *args, **options):
        for test_history in DiagnosticTestHistory.objects.all():
            test_property = TestPropertyEstimate.objects.get(test__id=test_history.test.pk, is_default=True)
            test_history.adjusted_date = test_history.test_date - relativedelta(days=test_property.mean_diagnostic_delay_days)
            test_history.save()
