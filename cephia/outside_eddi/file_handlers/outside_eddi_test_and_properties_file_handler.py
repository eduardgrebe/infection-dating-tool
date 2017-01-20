from outside_eddi.file_handlers.outside_eddi_file_handler import FileHandler
from cephia.file_handlers.handler_imports import *
import logging

from datetime import datetime
import datetime
from django.core.management import call_command

from outside_eddi.models import OutsideEddiSubject, OutsideEddiDiagnosticTest, OutsideEddiTestPropertyEstimate, TestPropertyMapping, OutsideEddiDiagnosticTestHistory
from django.db.models import Q
        
logger = logging.getLogger(__name__)

class TestsAndPropertiesFileHandler(FileHandler):

    def __init__(self, upload_file, *args, **kwargs):
        super(TestsAndPropertiesFileHandler, self).__init__(upload_file)

        self.registered_columns = [
            'Test name',
            'Test category',
            'Test property name',
            'Mean diagnostic delay',
            'S.E. mean diagnostic delay',
            'Comment'
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
                        test=OutsideEddiDiagnosticTest.objects.get(name=row_dict['Test name'])
                    except OutsideEddiDiagnosticTest.DoesNotExist:
                        test=OutsideEddiDiagnosticTest.objects.create(name=row_dict['Test name'])
                    
                    test.category = row_dict['Test category']
                    test.save()

                    try:
                        test_property=OutsideEddiTestPropertyEstimate.objects.get(
                            estimate_label=row_dict['Test property name']
                        )
                        test_property.mean_diagnostic_delay_days=float(row_dict['Mean diagnostic delay'])
                        test_property.comment=row_dict['Comment']
                        test_property.test=test
                        test_property.is_default=True
                        test_property.save()
                    except OutsideEddiTestPropertyEstimate.DoesNotExist:
                        test_property=OutsideEddiTestPropertyEstimate.objects.create(
                            estimate_label=row_dict['Test property name'],
                            mean_diagnostic_delay_days=float(row_dict['Mean diagnostic delay']),
                            comment=row_dict['Comment'],
                            test=test,
                            is_default=True
                        )


            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1

        return errors
