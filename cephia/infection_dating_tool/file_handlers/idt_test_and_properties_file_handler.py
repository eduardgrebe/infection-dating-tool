from infection_dating_tool.file_handlers.idt_file_handler import FileHandler
from cephia.file_handlers.handler_imports import *
import logging

from datetime import datetime
import datetime
from django.core.management import call_command

from infection_dating_tool.models import IDTSubject, IDTDiagnosticTest, IDTTestPropertyEstimate, TestPropertyMapping, IDTDiagnosticTestHistory, GrowthRateEstimate
from django.db.models import Q

logger = logging.getLogger(__name__)

CATEGORIES = {
    '1st Gen Lab Assay (Viral Lysate IgG sensitive Antibody)': '1st_gen_lab',
    '2nd Gen Lab Assay (Recombinant IgG sensitive Antibody)': '2nd_gen_lab',
    '2nd Gen Rapid Test': '2nd_gen_rapid',
    '3rd Gen Lab Assay (IgM sensitive Antibody)': '3rd_gen_lab',
    '3rd Gen Rapid Test': '3rd_gen_rapid',
    '4th Gen Lab Assay (p24 Ag/Ab Combo)': '4th_gen_lab',
    '4th Gen Rapid Test': '4th_gen_rapid',
    'DPP': 'dpp',
    'Immunofluorescence Assay': 'immunofluorescence_assay',
    'p24 Antigen': 'p24_antigen',
    'Viral Load': 'viral_load',
    'Western blot': 'western_blot',
}


class TestsAndPropertiesFileHandler(FileHandler):

    def __init__(self, upload_file, *args, **kwargs):
        super(TestsAndPropertiesFileHandler, self).__init__(upload_file)

        self.registered_columns = [
            'test_id',
            'test_name',
            'test_category',
            'estimate_label',
            'diagnostic_delay',
            'diagnostic_delay_sigma',
            'comment',
            'diagnostic_delay_mean',
            'diagnostic_delay_median',
            'diagnostic_delay_mean_se',
            'diagnostic_delay_mean_ci_lower',
            'diagnostic_delay_mean_ci_upper',
            'diagnostic_delay_range',
            'diagnostic_delay_iqr',
        ]

        self.header = self.file_rows[1]


    def import_data(self):
        errors = []

        from infection_dating_tool.models import IDTDiagnosticTest, IDTTestPropertyEstimate
        for row_num in range(self.num_rows):
            try:
                if row_num == 0:
                    viral_load_growth_rate = self.file_rows[row_num][1]
                    gre, created = GrowthRateEstimate.objects.get_or_create(user=None, growth_rate=viral_load_growth_rate)
                if row_num >= 2:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))

                    if not row_dict:
                        continue

                    try:
                        test = IDTDiagnosticTest.objects.get(pk=row_dict['test_id'], user__isnull=True)
                        test.name = row_dict['test_name']
                    except IDTDiagnosticTest.DoesNotExist:
                        test = IDTDiagnosticTest.objects.create(pk=row_dict['test_id'], name=row_dict['test_name'])

                    test.category = CATEGORIES[row_dict['test_category']]
                    test.save()
                    properties = test.properties.filter(user=None)

                    diagnostic_delay = None
                    if row_dict['diagnostic_delay']:
                        diagnostic_delay = float(row_dict['diagnostic_delay'])

                    if properties:
                        test_property = properties.first()
                        test_property.diagnostic_delay = diagnostic_delay
                        test_property.comment = row_dict['comment']
                        test_property.test = test
                        test_property.global_default = True
                        test_property.save()
                    else:
                        test_property = IDTTestPropertyEstimate.objects.create(
                            estimate_label=row_dict['estimate_label'],
                            diagnostic_delay=float(row_dict['diagnostic_delay']),
                            comment=row_dict['comment'],
                            test=test,
                            global_default=True
                        )

                    if not diagnostic_delay:
                        test_property.detection_threshold = float_or_none(row_dict['viral_load_detection_threshold'])

                    test_property.diagnostic_delay_sigma = float_or_none(row_dict['diagnostic_delay_sigma'])
                    test_property.diagnostic_delay_median = float_or_none(row_dict['diagnostic_delay_median'])
                    test_property.diagnostic_delay_mean_se = float_or_none(row_dict['diagnostic_delay_mean_se'])
                    test_property.diagnostic_delay_mean_ci_lower = float_or_none(row_dict['diagnostic_delay_mean_ci_lower'])
                    test_property.diagnostic_delay_mean_ci_upper = float_or_none(row_dict['diagnostic_delay_mean_ci_upper'])
                    test_property.diagnostic_delay_range = row_dict['diagnostic_delay_range'] or None
                    test_property.diagnostic_delay_iqr = row_dict['diagnostic_delay_iqr'] or None
                    test_property.save()


            except Exception, e:
                logger.exception(e)
                return e

        return errors


def float_or_none(s):
    if not s and s != 0:
        return None
    else:
        return float(s)
