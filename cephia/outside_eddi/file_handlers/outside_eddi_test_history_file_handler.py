from cephia.file_handlers.file_handler import FileHandler
from cephia.file_handlers.handler_imports import *
import logging

from datetime import datetime
import datetime
from django.core.management import call_command

from outside_eddi.models import OutsideEddiSubject, OutsideEddiDiagnosticTest, OutsideEddiTestPropertyEstimate, TestPropertyMapping, OutsideEddiDiagnosticTestHistory
from django.db.models import Q
        
logger = logging.getLogger(__name__)

class OutsideEddiFileHandler(FileHandler):

    def __init__(self, upload_file, *args, **kwargs):
        super(OutsideEddiFileHandler, self).__init__(upload_file)

        self.registered_columns = [
            'subject_id',
            'test_date',
            'test_code',
            'test_result',
            'test_source',
            'protocol'
        ]

    def validate(self):
        valid_results = ('positive', 'pos', 'negative', 'neg', '+', '-')
        headers = [u'', u'SubjectId', u'TestDate', u'TestCode', u'TestResult']
        errors = []
        from outside_eddi.models import OutsideEddiSubject
        if self.header != headers:
            errors.append("Incorrect headers used. It should be SubjectId, TestDate, TestCode, TestResult")
        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    
                    if not row_dict:
                        continue

                    if not validate_date(row_dict['TestDate']):
                        errors.append("row " + str(row_num) + ": Incorrect date format, should be YYYY-MM-DD")

                    if not row_dict['TestResult'].lower() in valid_results:
                        errors.append("row " + str(row_num) + ": Incorrect result format used")

            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1

        return errors

    def save_data(self, user):
        tests = OutsideEddiDiagnosticTest.objects.filter(Q(user=self.upload_file.user) | Q(user=None))
        test_names = [x.name for x in tests]
        mapping_needed = []
        pos_results = ('positive', 'pos', '+')
        neg_results = ('negative', 'neg', '-')
        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    if not row_dict:
                        continue

                    if OutsideEddiSubject.objects.filter(subject_label=row_dict['SubjectId'], user=user).exists():
                        subject = OutsideEddiSubject.objects.get(
                            subject_label=row_dict['SubjectId'],
                            user=user
                        )
                    else:
                        subject = OutsideEddiSubject.objects.create(
                            subject_label=row_dict['SubjectId'],
                            user=user
                        )
                    
                    test_history_row = OutsideEddiDiagnosticTestHistory.objects.create(subject=subject, data_file=self.upload_file)
                    test_history_row.test_date = row_dict['TestDate']
                    test_history_row.test_code = row_dict['TestCode']

                    mapping = check_mapping(test_history_row.test_code, test_names, user)
                    if mapping == False:
                        mapping_needed.append("row " + str(row_num) + ": Mapping needed for test code: " + test_history_row.test_code)

                    if row_dict['TestResult'].lower() in pos_results:
                        test_history_row.test_result = 'Positive'
                    elif row_dict['TestResult'].lower() in neg_results:
                        test_history_row.test_result = 'Negative'
                    test_history_row.save()

            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                import pdb;pdb.set_trace()
                self.upload_file.save()
                return 0, 1

        return mapping_needed

def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def check_mapping(test_code, tests, user):
    if test_code in tests:
        if TestPropertyMapping.objects.filter(code=test_code, user=user).exists():
            mapping = TestPropertyMapping.objects.get(code=test_code, user=user)
        else:
            test = OutsideEddiDiagnosticTest.objects.get(name=test_code)
            test_property = test.get_default_property()
            
            mapping = TestPropertyMapping.objects.create(
                code=str(test_code),
                test=test,
                test_property=test_property,
                user=user
            )
    else:
        if TestPropertyMapping.objects.filter(code=test_code, user=user).exists():
            mapping = TestPropertyMapping.objects.get(code=test_code, user=user)
        else:
            mapping = TestPropertyMapping.objects.create(
                code=test_code,
                user=user
            )
    if not mapping.test or not mapping.test_property:
        return False
    else:
        return True