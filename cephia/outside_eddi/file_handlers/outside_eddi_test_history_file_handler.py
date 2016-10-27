from cephia.file_handlers.file_handler import FileHandler
from cephia.file_handlers.handler_imports import *
import logging

from datetime import datetime
import datetime
from django.core.management import call_command

logger = logging.getLogger(__name__)

valid_results = ('positive', 'pos', 'negative', 'neg', '+', '-')
headers = [u'', u'SubjectId', u'TestDate', u'TestCode', u'TestResult']

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

                    if not validate(row_dict['TestDate']):
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
        from outside_eddi.models import OutsideEddiSubject
        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    if not row_dict:
                        continue

                    subject_row = OutsideEddiSubject.objects.create(subject_label=row_dict['SubjectId'])
                    subject_row.test_date = row_dict['TestDate']
                    subject_row.test_code = row_dict['TestCode']
                    subject_row.test_result = row_dict['TestResult']
                    subject_row.save()

            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False
        # raise ValueError("Incorrect data format, should be YYYY-MM-DD")
