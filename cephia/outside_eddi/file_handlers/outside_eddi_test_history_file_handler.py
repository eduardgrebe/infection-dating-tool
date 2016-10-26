from cephia.file_handlers.file_handler import FileHandler
from cephia.file_handlers.handler_imports import *
import logging
from datetime import datetime
import datetime
from django.core.management import call_command

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

    def save_data(self):
        from outside_eddi.models import OutsideEddiSubject

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    if not row_dict:
                        continue

                    subject_row = OutsideEddiSubject.objects.create(subject_label=row_dict['SubjectId'])

                    if validate(row_dict['TestDate']):
                        subject_row.test_date = row_dict['TestDate']
                    else:
                        self.upload_file.message = "row " + str(row_num) + ": Incorrect date format, should be YYYY-MM-DD"
                        self.upload_file.save()

                    subject_row.test_code = row_dict['TestCode']
                    subject_row.test_result = row_dict['TestResult']
                    subject_row.test_source = row_dict['TestSource']
                    subject_row.protocol = row_dict['Protocol']
                    subject_row.save()

            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1

    # def parse(self):
    #     from cephia.models import TreatmentStatusUpdateRow
        
    #     rows_inserted = 0
    #     rows_failed = 0
        
    #     for row_num in range(self.num_rows):
    #         try:
    #             if row_num >= 1:
    #                 row_dict = dict(zip(self.header, self.file_rows[row_num]))
    #                 if not row_dict:
    #                     continue
                    
    #                 treatment_status_update_row = TreatmentStatusUpdateRow.objects.create(subject_label=row_dict['subject_label'], fileinfo=self.upload_file)
                        
    #                 treatment_status_update_row.subject_label = row_dict['subject_label']
    #                 treatment_status_update_row.source_study = row_dict['source_study']
    #                 treatment_status_update_row.art_initiation_date_yyyy = row_dict['art_initiation_date_yyyy']
    #                 treatment_status_update_row.art_initiation_date_mm = row_dict['art_initiation_date_mm']
    #                 treatment_status_update_row.art_initiation_date_dd = row_dict['art_initiation_date_dd']
    #                 treatment_status_update_row.art_interruption_date_yyyy = row_dict['art_interruption_date_yyyy']
    #                 treatment_status_update_row.art_interruption_date_mm = row_dict['art_interruption_date_mm']
    #                 treatment_status_update_row.art_interruption_date_dd = row_dict['art_interruption_date_dd']
    #                 treatment_status_update_row.art_resumption_date_yyyy = row_dict['art_resumption_date_yyyy']
    #                 treatment_status_update_row.art_resumption_date_mm = row_dict['art_resumption_date_mm']
    #                 treatment_status_update_row.art_resumption_date_dd = row_dict['art_resumption_date_dd']
    #                 treatment_status_update_row.fileinfo=self.upload_file
    #                 treatment_status_update_row.state = 'pending'
    #                 treatment_status_update_row.error_message = ''
    #                 treatment_status_update_row.save()

    #                 rows_inserted += 1
    #         except Exception, e:
    #             logger.exception(e)
    #             self.upload_file.message = "row " + str(row_num) + ": " + e.message
    #             self.upload_file.save()
    #             return 0, 1

    #     return rows_inserted, rows_failed

    # def validate(self):
    #     from cephia.models import Ethnicity, Subtype, Country, Subject, TreatmentStatusUpdateRow

    #     rows_validated = 0
    #     rows_failed = 0
    #     default_less_date = datetime.now().date() - relativedelta(years=75)
    #     default_more_date = datetime.now().date() + relativedelta(years=75)
    #     pending_rows = TreatmentStatusUpdateRow.objects.filter(fileinfo=self.upload_file, state='pending')

    #     for treatment_status_update_row in pending_rows:
    #         try:
    #             error_msg = ''
    #             self.register_dates(treatment_status_update_row.model_to_dict())

    #             if not Subject.objects.filter(subject_label=treatment_status_update_row.subject_label).exists():
    #                 error_msg += 'could not find subject for label %s.\n' % treatment_status_update_row.subject_label

    #             if not self.registered_dates.get('art_interruption_date', default_more_date) > self.registered_dates.get('art_initiation_date', default_less_date):
    #                 error_msg += 'art_interruption_date must be after art_initiation_date.\n'
        
    #             if not self.registered_dates.get('art_resumption_date', default_more_date) > self.registered_dates.get('art_interruption_date', default_less_date):
    #                 error_msg += 'art_resumption_date must be after art_interruption_date.\n'


    #             if error_msg:
    #                 raise Exception(error_msg)
                
    #             treatment_status_update_row.state = 'validated'
    #             treatment_status_update_row.error_message = ''
    #             rows_validated += 1
    #             treatment_status_update_row.save()
    #         except Exception, e:
    #             logger.exception(e)
    #             treatment_status_update_row.state = 'error'
    #             treatment_status_update_row.error_message = e.message
    #             treatment_status_update_row.save()
    #             rows_failed += 1
    #             continue
            
    #     return rows_validated, rows_failed
        
    # def process(self):
    #     from cephia.models import Ethnicity, Subtype, Country, Subject, TreatmentStatusUpdateRow, Study
        
    #     rows_inserted = 0
    #     rows_failed = 0

    #     for treatment_status_update_row in TreatmentStatusUpdateRow.objects.filter(fileinfo=self.upload_file, state='validated'):
    #         try:
    #             with transaction.atomic():
    #                 self.register_dates(treatment_status_update_row.model_to_dict())
                    
    #                 subject = Subject.objects.get(
    #                     subject_label=treatment_status_update_row.subject_label
    #                 )

    #                 subject_data = dict(
    #                     source_study=Study.objects.get(name=treatment_status_update_row.source_study),
    #                     art_initiation_date = self.registered_dates.get('art_initiation_date', None),
    #                     art_interruption_date = self.registered_dates.get('art_interruption_date', None),
    #                     art_resumption_date = self.registered_dates.get('art_resumption_date', None)
    #                 )

    #                 [setattr(subject, k,v) for k,v in subject_data.iteritems()]
                    
    #                 subject.save()

    #                 treatment_status_update_row.state = 'processed'
    #                 treatment_status_update_row.error_message = ''
    #                 treatment_status_update_row.date_processed = timezone.now()
    #                 treatment_status_update_row.subject = subject
    #                 rows_inserted += 1
    #                 treatment_status_update_row.save()
    #         except Exception, e:
    #             logger.exception(e)
    #             treatment_status_update_row.state = 'error'
    #             treatment_status_update_row.error_message = e.message
    #             treatment_status_update_row.save()
    #             rows_failed += 1
    #             continue
    #     call_command('treatment_status_update')
    #     return rows_inserted, rows_failed

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False
        # raise ValueError("Incorrect data format, should be YYYY-MM-DD")
