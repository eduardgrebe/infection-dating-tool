from cephia.file_handlers.file_handler import FileHandler
from cephia.file_handlers.handler_imports import *
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
                                   'TestSource', # remove?
                                   'Protocol'] # remove?

    def parse(self):
        from outside_eddi.models import OutsideEddiDiagnosticTestHistoryRow

        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    
                    test_history_row = OutsideEddiDiagnosticTestHistoryRow.objects.create(subject=row_dict['SubjectId'],
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
        from outside_eddi.models import (OutsideEddiDiagnosticTestHistoryRow, OutsideEddiProtocolLookup,
                                        OutsideEddiTestPropertyEstimate, OutsideEddiDiagnosticTestHistory)

        rows_validated = 0
        rows_failed = 0
        
        for test_history_row in OutsideEddiDiagnosticTestHistoryRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''
                protocol = None

                try:
                    subject = Subject.objects.get(subject_label=test_history_row.subject)
                except Subject.DoesNotExist:
                    error_msg += "Subject not recognised.\n"

                try:
                    protocol = OutsideEddiProtocolLookup.objects.get(name=test_history_row.test_code, protocol=test_history_row.protocol)
                except OutsideEddiProtocolLookup.DoesNotExist:
                    error_msg += "Protocol not recognised.\n"

                if not datetime.strptime(test_history_row.test_date, "%Y-%m-%d").date() < datetime.now().date():
                    error_msg += 'test_date must be before today.\n'

                if not datetime.strptime(test_history_row.test_date, "%Y-%m-%d").date() > datetime.strptime('1980-01-01', "%Y-%m-%d").date():
                    error_msg += 'test_date must be after 1 Jan 1980.\n'

                try:
                    if protocol:
                        OutsideEddiTestPropertyEstimate.objects.get(test__id=protocol.test.pk, is_default=True)
                except OutsideEddiTestPropertyEstimate.DoesNotExist:
                    error_msg += "Property Estimate not recognised.\n"


                if OutsideEddiDiagnosticTestHistory.objects.filter(subject__subject_label=test_history_row.subject, ignore=True).exists():
                    error_msg += "Cannot overwrite test history data that has already been edited.\n"
                    
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
        from cephia.models import Subject, SubjectEDDI
        from outside_eddi.models import OutsideEddiDiagnosticTestHistoryRow, OutsideEddiProtocolLookup, OutsideEddiTestPropertyEstimate
        
        rows_inserted = 0
        rows_failed = 0

        try:
            with transaction.atomic():
                excluded_subjects = OutsideEddiDiagnosticTestHistoryRow.objects.values_list('subject', flat=True).filter(fileinfo=self.upload_file, state='error').distinct()
                
                for subject_label in excluded_subjects:
                    if not OutsideEddiDiagnosticTestHistory.objects.filter(subject__subject_label=subject_label, ignore=True).exists():
                        OutsideEddiDiagnosticTestHistory.objects.filter(subject__subject_label=subject_label).delete()
                    else:
                        continue
                    
                for subject_row_error in OutsideEddiDiagnosticTestHistoryRow.objects.filter(subject__in=excluded_subjects, state='validated', fileinfo=self.upload_file):
                    subject_row_error.state = 'error'
                    subject_row_error.error_message = "One or more records for this subject have errors"
                    subject_row_error.save()
        except Exception, e:
            pass

        for subject_label in OutsideEddiDiagnosticTestHistoryRow.objects.values_list('subject', flat=True).filter(fileinfo=self.upload_file, state='validated').distinct():
            with transaction.atomic():
                OutsideEddiDiagnosticTestHistory.objects.filter(subject__subject_label=subject_label).delete()
                try:
                    for test_history_row in OutsideEddiDiagnosticTestHistoryRow.objects.filter(subject=subject_label, fileinfo=self.upload_file, state='validated'):
                        test_history = OutsideEddiDiagnosticTestHistory.objects.create(subject=Subject.objects.get(subject_label=test_history_row.subject),
                                                                            test_date=datetime.strptime(test_history_row.test_date, "%Y-%m-%d").date(),
                                                                            test_result=test_history_row.test_result,
                                                                            test=ProtocolLookup.objects.get(name=test_history_row.test_code,
                                                                                                            protocol=test_history_row.protocol).test)

                        if not test_history.subject.subject_eddi:
                            test_history.subject.subject_eddi = SubjectEDDI.objects.create()
                            test_history.subject.save()
                        else:
                            test_history.subject.subject_eddi.ep_ddi = None
                            test_history.subject.subject_eddi.lp_ddi = None
                            test_history.subject.subject_eddi.interval_size = None
                            test_history.subject.subject_eddi.eddi = None

                        test_history.subject.subject_eddi.recalculate = True
                        test_history.subject.subject_eddi.save()
                        test_property = OutsideEddiTestPropertyEstimate.objects.get(test__id=test_history.test.pk, is_default=True)
                        test_history.adjusted_date = test_history.test_date - relativedelta(days=test_property.mean_diagnostic_delay_days)
                        test_history.save()

                        test_history_row.state = 'processed'
                        test_history_row.error_message = ''
                        test_history_row.date_processed = timezone.now()
                        test_history_row.test_history = test_history
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
