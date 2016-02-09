from file_handler import FileHandler
from handler_imports import *
import logging
from datetime import datetime
from django.core.management import call_command

logger = logging.getLogger(__name__)


class TestHistoryFileHandler(FileHandler):

    def __init__(self, upload_file):
        super(TestHistoryFileHandler, self).__init__(upload_file)

        self.registered_columns = ['SubjectId',
                                   'TestCode',
                                   'TestDate',
                                   'TestResult',
                                   'TestSource',
                                   'Protocol']

    def parse(self):
        from diagnostics.models import DiagnosticTestHistoryRow

        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    
                    test_history_row = DiagnosticTestHistoryRow.objects.create(subject=row_dict['SubjectId'],
                                                                               test_date=row_dict['TestDate'],
                                                                               test_code=row_dict['TestCode'],
                                                                               test_result=row_dict['TestResult'],
                                                                               source=row_dict['TestSource'],
                                                                               protocol=row_dict['Protocol'],
                                                                               state='pending',
                                                                               fileinfo=self.upload_file)

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1

        return rows_inserted, rows_failed
    
    def validate(self):
        from cephia.models import Subject
        from diagnostics.models import DiagnosticTestHistoryRow, ProtocolLookup, TestPropertyEstimate

        rows_validated = 0
        rows_failed = 0
        
        for test_history_row in DiagnosticTestHistoryRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''
                protocol = None

                try:
                    subject = Subject.objects.get(subject_label=test_history_row.subject)
                except Subject.DoesNotExist:
                    error_msg += "Subject not recognised.\n"

                try:
                    protocol = ProtocolLookup.objects.get(name=test_history_row.test_code, protocol=test_history_row.protocol)
                except ProtocolLookup.DoesNotExist:
                    error_msg += "Protocol not recognised.\n"

                if not datetime.strptime(test_history_row.test_date, "%Y-%m-%d").date() < datetime.now().date():
                    error_msg += 'test_date must be before today.\n'

                if not datetime.strptime(test_history_row.test_date, "%Y-%m-%d").date() > datetime.strptime('1980-01-01', "%Y-%m-%d").date():
                    error_msg += 'test_date must be after 1 Jan 1980.\n'

                try:
                    if protocol:
                        TestPropertyEstimate.objects.get(test__id=protocol.test.pk, is_default=True)
                except TestPropertyEstimate.DoesNotExist:
                    error_msg += "Property Estimate not recognised.\n"

                if error_msg:
                    raise Exception(error_msg)

                test_history_row.state = 'validated'
                test_history_row.error_message = ''
                rows_validated += 1
                test_history_row.save()
            except Exception, e:
                logger.exception(e)
                test_history_row.state = 'error'
                test_history_row.error_message = e.message
                rows_failed += 1
                test_history_row.save()
                continue

        return rows_validated, rows_failed

    def process(self):
        from cephia.models import Subject
        from diagnostics.models import DiagnosticTestHistoryRow, DiagnosticTestHistory, ProtocolLookup, TestPropertyEstimate
        
        rows_inserted = 0
        rows_failed = 0

        try:
            with transaction.atomic():
                excluded_subjects = DiagnosticTestHistoryRow.objects.values_list('subject', flat=True).filter(fileinfo=self.upload_file, state='error').distinct()
                
                for subject_label in excluded_subjects:
                    DiagnosticTestHistory.objects.filter(subject__subject_label=subject_label).delete()
                    
                for subject_row_error in DiagnosticTestHistoryRow.objects.filter(subject__in=excluded_subjects, state='validated', fileinfo=self.upload_file):
                    subject_row_error.state = 'error'
                    subject_row_error.error_message = "One or more records for this subject have errors"
                    subject_row_error.save()
        except Exception, e:
            pass
        
        for subject_label in DiagnosticTestHistoryRow.objects.values_list('subject', flat=True).filter(fileinfo=self.upload_file, state='validated').distinct():
            with transaction.atomic():
                import pdb; pdb.set_trace()
                DiagnosticTestHistory.objects.filter(subject__subject_label=subject_label).delete()
                try:        
                    for test_history_row in DiagnosticTestHistoryRow.objects.filter(subject=subject_label, fileinfo=self.upload_file, state='validated'):
                        test_history = DiagnosticTestHistory.objects.create(subject=Subject.objects.get(subject_label=test_history_row.subject),
                                                                            test_date=datetime.strptime(test_history_row.test_date, "%Y-%m-%d").date(),
                                                                            test_result=test_history_row.test_result,
                                                                            test=ProtocolLookup.objects.get(name=test_history_row.test_code,
                                                                                                            protocol=test_history_row.protocol).test)
                        
                        test_history.subject.subject_eddi.recalculate = True
                        test_history.subject.subject_eddi.save()
                        test_property = TestPropertyEstimate.objects.get(test__id=test_history.test.pk, is_default=True)
                        test_history.adjusted_date = test_history.test_date - relativedelta(days=test_property.mean_diagnostic_delay_days)
                        test_history.save()
                        
                        test_history_row.state = 'processed'
                        test_history_row.error_message = ''
                        test_history_row.date_processed = timezone.now()
                        test_history_row.save()

                        rows_inserted += 1
                except Exception, e:
                    logger.exception(e)
                    test_history_row.state = 'error'
                    test_history_row.error_message = e.message
                    test_history_row.save()
                    rows_failed += 1
                    continue

        call_command('eddi_update', 'flagged')
        self.upload_file.state = 'processed'
        self.upload_file.save()
        return rows_inserted, rows_failed
