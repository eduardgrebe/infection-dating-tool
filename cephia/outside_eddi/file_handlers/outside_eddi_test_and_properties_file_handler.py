from outside_eddi.file_handlers.outside_eddi_file_handler import FileHandler
from cephia.file_handlers.handler_imports import *
import logging

from datetime import datetime
import datetime
from django.core.management import call_command

from outside_eddi.models import OutsideEddiSubject, OutsideEddiDiagnosticTest, OutsideEddiTestPropertyEstimate, TestPropertyMapping, OutsideEddiDiagnosticTestHistory
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
            'comment',
            'diagnostic_delay_mean',
            'diagnostic_delay_median',
            'diagnostic_delay_mean_se',
            'diagnostic_delay_mean_ci_lower',
            'diagnostic_delay_mean_ci_upper',
            'diagnostic_delay_range',
            'diagnostic_delay_iqr',
        ]


    def import_data(self):
        errors = []
        
        from outside_eddi.models import OutsideEddiDiagnosticTest, OutsideEddiTestPropertyEstimate
        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))

                    if not row_dict:
                        continue

                    try:
                        test=OutsideEddiDiagnosticTest.objects.get(pk=row_dict['test_id'], user__isnull=True)
                        test.name = row_dict['test_name']
                    except OutsideEddiDiagnosticTest.DoesNotExist:
                        test=OutsideEddiDiagnosticTest.objects.create(pk=row_dict['test_id'], name=row_dict['test_name'])

                    test.category = CATEGORIES[row_dict['test_category']]
                    test.save()
                    properties = test.properties.filter(user=None)

                    if properties:
                        test_property = properties.first()
                        test_property.diagnostic_delay=float(row_dict['diagnostic_delay'])
                        test_property.comment=row_dict['comment']
                        test_property.test=test
                        test_property.is_default=True
                        test_property.save()
                    else:
                        test_property=OutsideEddiTestPropertyEstimate.objects.create(
                            estimate_label=row_dict['estimate_label'],
                            diagnostic_delay=float(row_dict['diagnostic_delay']),
                            comment=row_dict['comment'],
                            test=test,
                            is_default=True
                        )

                    test_property.diagnostic_delay_median=row_dict['diagnostic_delay_median'] or None
                    test_property.diagnostic_delay_mean_se=row_dict['diagnostic_delay_mean_se'] or None
                    test_property.diagnostic_delay_mean_ci_lower=row_dict['diagnostic_delay_mean_ci_lower'] or None
                    test_property.diagnostic_delay_mean_ci_upper=row_dict['diagnostic_delay_mean_ci_upper'] or None
                    test_property.diagnostic_delay_range=row_dict['diagnostic_delay_range'] or None
                    test_property.diagnostic_delay_iqr=row_dict['diagnostic_delay_iqr'] or None
                    test_property.save()


            except Exception, e:
                logger.exception(e)
                return e

        return errors
