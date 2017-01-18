from django.core.management.base import BaseCommand, CommandError
from cephia.models import DiagnosticTest, TestPropertyEstimate
from outside_eddi.models import OutsideEddiDiagnosticTest, OutsideEddiTestPropertyEstimate
from django.db.models import F
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update or create global tests and test properties for the Cephia Infection Dating Tool'

    def handle(self, *args, **options):
        global_tests = DiagnosticTest.objects.all()

        for test in tests:
            outside_eddi_test = OutsideEddiDiagnosticTest.objects.get_or_create(name = test.name,
                                                                                description = test.description)


        test_properties = TestPropertyEstimate.objects.all()

        for prop in test_properties:
            test_name = prop.test.name
            test = OutsideEddiDiagnosticTest.objects.filter(name=test_name).first()

            outside_eddi_test_property = OutsideEddiTestPropertyEstimate.objects.get_or_create(test = test,
                                                                                               estimate_label=prop.estimate_label,
                                                                                               estimate_type=prop.estimate_type,
                                                                                               mean_diagnostic_delay_days=prop.mean_diagnostic_delay_days,
                                                                                               diagnostic_delay_median=prop.diagnostic_delay_median,
                                                                                               foursigma_diagnostic_delay_days=prop.foursigma_diagnostic_delay_days,
                                                                                               time0_ref=prop.time0_ref,
                                                                                               comment=prop.comment,
                                                                                               reference=prop.reference)

            if prop.is_default == True:
                outside_eddi_test_property.is_default = True
                outside_eddi_test_property.active_property = True

            outside_eddi_test_property.save()

