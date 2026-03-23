from infection_dating_tool.file_handlers.idt_file_handler import FileHandler
from cephia.file_handlers.handler_imports import *
import logging

from datetime import datetime
import datetime
from django.core.management import call_command

from infection_dating_tool.models import IDTSubject, IDTDiagnosticTest, IDTTestPropertyEstimate, TestPropertyMapping, IDTDiagnosticTestHistory
from django.db.models import Q

logger = logging.getLogger(__name__)

class IDTFileHandler(FileHandler):

    def __init__(self, upload_file, *args, **kwargs):
        super(IDTFileHandler, self).__init__(upload_file)

        self.registered_columns = [
            'Subject',
            'Date',
            'Test',
            'Result',
        ]


    def validate(self):
        valid_results = ('positive', 'pos', 'negative', 'neg', '+', '-')
        headers = [u'Subject', u'Date', u'Test', u'Result']
        errors = []
        from infection_dating_tool.models import IDTSubject

        if not set(headers) < set(self.header) and not set(headers) == set(self.header):
            errors.append("Your headers should contain Subject, Date, Test and Result")
        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))

                    row_contains_data = False
                    for field in self.file_rows[row_num]:
                        if field:
                            row_contains_data = True

                    if not row_contains_data:
                        continue

                    if not row_dict:
                        continue

                    if not validate_date(row_dict['Date']):
                        errors.append("row " + str(row_num) + ": Incorrect date format, should be YYYY-MM-DD")

                    if not row_dict['Result'].lower() in valid_results:
                        errors.append("row " + str(row_num) + ": Incorrect result format used")

            except Exception, e:
                logger.exception(e)
                # self.upload_file.message = "row " + str(row_num) + ": " + e.message
                # self.upload_file.save()
                errors.append("row " + str(row_num) + ": %s" %e)
                return errors

        return errors


    def save_data(self, user):
        pos_results = ('positive', 'pos', '+')
        neg_results = ('negative', 'neg', '-')
        errors = []

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))

                    row_contains_data = False
                    for field in self.file_rows[row_num]:
                        if field:
                            row_contains_data = True

                    if not row_contains_data:
                        continue

                    if not row_dict:
                        continue

                    if IDTSubject.objects.filter(subject_label=row_dict['Subject'], user=user).exists():
                        subject = IDTSubject.objects.get(
                            subject_label=row_dict['Subject'],
                            user=user
                        )
                    else:
                        subject = IDTSubject.objects.create(
                            subject_label=row_dict['Subject'],
                            user=user
                        )
                        subject.save()

                    test_history_row = IDTDiagnosticTestHistory.objects.create(subject=subject, data_file=self.upload_file)

                    test_history_row.test_date = row_dict['Date']
                    test_history_row.test_code = row_dict['Test']

                    if row_dict['Result'].lower() in pos_results:
                        test_history_row.test_result = 'Positive'
                    elif row_dict['Result'].lower() in neg_results:
                        test_history_row.test_result = 'Negative'
                    test_history_row.save()

            except Exception, e:
                logger.exception(e)
                # self.upload_file.message = "row " + str(row_num) + ": " + e.message
                # self.upload_file.save()
                errors.append("row " + str(row_num) + ": %s" %e)
                return errors


def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        # if not date_text:
        #     return True
        return False

def check_mapping(test_code, tests, user):
    if test_code in tests:
        if TestPropertyMapping.objects.filter(code=test_code, user=user).exists():
            mapping = TestPropertyMapping.objects.get(code=test_code, user=user)
        else:
            test = IDTDiagnosticTest.objects.get(name=test_code)
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


def create_mapping(test_code, tests, user):
    if test_code in tests:
        if IDTTestPropertyMapping.objects.filter(code=test_code, user=user).exists():
            mapping = TestPropertyMapping.objects.get(code=test_code, user=user)
        else:
            test = IDTDiagnosticTest.objects.get(name=test_code)
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
