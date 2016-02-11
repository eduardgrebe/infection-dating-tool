from file_handler import FileHandler
from handler_imports import *
import logging

logger = logging.getLogger(__name__)

class TestPropertyFileHandler(FileHandler):
    upload_file = None
    
    def __init__(self, upload_file):
        super(TestPropertyFileHandler, self).__init__(upload_file)

        self.registered_columns = ['id',
                                   'test',
                                   'estimate_type',
                                   'estimate_category',
                                   'is_default',
                                   'diagnostic_delay_mean',
                                   'diagnostic_delay_median',
                                   'diagnostic_delay_4sigma',
                                   'time0_ref',
                                   'comment',
                                   'reference']

    def process(self):
        from diagnostics.models import TestPropertyEstimate, DiagnosticTest
        
        rows_inserted = 0
        rows_failed = 0

        TestPropertyEstimate.objects.all().delete()
        
        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    test_property = TestPropertyEstimate.objects.create(test=DiagnosticTest.objects.get(pk=row_dict['test']),
                                                                        estimate_label=row_dict['estimate_label'],
                                                                        estimate_type=row_dict['estimate_type'],
                                                                        is_default=self.get_bool(row_dict['is_default']),
                                                                        time0_ref=row_dict['time0_ref'],
                                                                        comment=row_dict['comment'],
                                                                        reference=row_dict['reference'])

                    if row_dict['diagnostic_delay_mean']:
                        test_property.mean_diagnostic_delay_days = float(row_dict['diagnostic_delay_mean'])
                    else:
                        test_property.mean_diagnostic_delay_days = None

                    if row_dict['diagnostic_delay_4sigma']:
                        test_property.foursigma_diagnostic_delay_days = float(row_dict['diagnostic_delay_4sigma'])
                    else:
                        test_property.foursigma_diagnostic_delay_days = None
                        
                    if row_dict['diagnostic_delay_median']:
                        test_property.foursigma_diagnostic_delay_median = float(row_dict['diagnostic_delay_median'])
                    else:
                        test_property.foursigma_diagnostic_delay_median = None

                    test_property.save()

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "Row " + str(row_num) + ": " + e.message
                self.upload_file.state = 'error'
                self.upload_file.save()
                return 0, 1

        self.upload_file.state = 'processed'
        self.upload_file.save()
        return rows_inserted, rows_failed
