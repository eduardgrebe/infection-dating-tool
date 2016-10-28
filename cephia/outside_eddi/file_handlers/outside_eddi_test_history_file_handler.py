from cephia.file_handlers.file_handler import FileHandler
from cephia.file_handlers.handler_imports import *
import logging

from datetime import datetime
import datetime
from django.core.management import call_command

from outside_eddi.models import OutsideEddiSubject, OutsideEddiDiagnosticTest, OutsideEddiTestPropertyEstimate, TestPropertyMapping
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
        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    if not row_dict:
                        continue

                    subject = OutsideEddiSubject.objects.create(
                        subject_label=row_dict['SubjectId'],
                        data_file=self.upload_file
                    )
                    subject.test_date = row_dict['TestDate']
                    subject.test_code = row_dict['TestCode']

                    mapping = get_or_create_map(subject.test_code, test_names, user)
                    
                    subject.test_result = row_dict['TestResult']
                    subject.save()

            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1

def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def get_or_create_map(test_code, tests, user):
    if test_code in tests:
        if TestPropertyMapping.objects.filter(code=test_code, user=user).exists():
            mapping = TestPropertyMapping.objects.get(code=test_code, user=user)
        else:
            test = OutsideEddiDiagnosticTest.objects.get(name=test_code)
            test_property = test.get_default_property()
            mapping = TestPropertyMapping.objects.create(
                code=test_code,
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
    return mapping
