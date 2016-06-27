from file_handler import FileHandler
from handler_imports import *
import logging
from lib import log_exception

logger = logging.getLogger(__name__)

class VisitFileHandler(FileHandler):
    upload_file = None
    
    def __init__(self, upload_file):
        super(VisitFileHandler, self).__init__(upload_file)

        self.registered_columns = ['subject_label',
                                   'visitdate_yyyy',
                                   'visitdate_mm',
                                   'visitdate_dd',
                                   'visit_hivstatus',
                                   'source_study',
                                   'cd4_count',
                                   'vl',
                                   'scopevisit_ec',
                                   'pregnant',
                                   'hepatitis',
                                   'artificial']

    def parse(self):
        from cephia.models import VisitRow
        
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))

                    if row_dict.get('id', None):
                        try:
                            visit_row = VisitRow.objects.get(pk=row_dict['id'], state__in=['error', 'pending', 'validated', 'imported'])
                        except VisitRow.DoesNotExist, e:
                            continue
                    else:
                        visit_row = VisitRow.objects.create(subject_label=row_dict['subject_label'], fileinfo=self.upload_file)

                    visit_row.subject_label = row_dict['subject_label']
                    visit_row.visitdate_yyyy = row_dict['visitdate_yyyy']
                    visit_row.visitdate_mm = row_dict['visitdate_mm']
                    visit_row.visitdate_dd = row_dict['visitdate_dd']
                    visit_row.visit_hivstatus = row_dict['visit_hivstatus']
                    visit_row.source_study = row_dict['source_study']
                    visit_row.cd4_count = row_dict['cd4_count']
                    visit_row.vl = row_dict['vl']
                    visit_row.scopevisit_ec = row_dict['scopevisit_ec']
                    visit_row.pregnant = row_dict['pregnant']
                    visit_row.hepatitis = row_dict['hepatitis']
                    visit_row.artificial = row_dict['artificial']

                    visit_row.fileinfo = self.upload_file
                    visit_row.state = 'pending'
                    visit_row.save()

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1

        return rows_inserted, rows_failed

    def validate(self):
        from cephia.models import Visit, VisitRow, Subject

        default_less_date = datetime.now().date() - relativedelta(years=75)
        default_more_date = datetime.now().date() + relativedelta(years=75)
        rows_validated = 0
        rows_failed = 0

        for visit_row in VisitRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''
                self.register_dates(visit_row.model_to_dict())
                try:
                    subject = Subject.objects.get(subject_label=visit_row.subject_label)
                except Subject.DoesNotExist:
                    subject = None

                first_visit = Visit.objects.filter(subject_label=visit_row.subject_label).order_by('visit_date').first()
                already_exists = Visit.objects.filter(subject_label=visit_row.subject_label, visit_date=self.registered_dates['visitdate']).exists()

                if already_exists:
                    raise Exception("Visit already exists.")

                if subject:
                    if not self.registered_dates.get('visitdate', default_less_date) >= (subject.cohort_entry_date or default_less_date):
                        error_msg += 'visit_date cannot be before cohort_entry_date.\n'

                    if visit_row.pregnant == 'Y' and subject.sex == 'M':
                        error_msg += 'Male subjects cannot be marked as pregnant.\n'

                    if subject.cohort_entry_hiv_status == 'P' and visit_row.visit_hivstatus == 'N':
                        error_msg += 'visit_hiv_status cannot be "negative" if subject has a positive cohort_entry_hiv_status.\n'

                    # This should be replaced by a check that the source_study field corresponds to the subject's source_study.
                    #if first_visit:
                    #    if first_visit.source_study.name != visit_row.source_study:
                    #        error_msg += 'Reported source_study for visit does not match source_study of first visit for subject.\n'

                if not self.registered_dates['visitdate'] < datetime.now().date():
                    error_msg += 'visit_date must be before today.\n'

                if visit_row.scopevisit_ec and visit_row.source_study != 'SCOPE':
                    error_msg += 'scope_visit_ec must be null if source study is not "SCOPE".\n'
        
                if error_msg:
                    raise Exception(error_msg)
                
                visit_row.state = 'validated'
                visit_row.error_message = ''
                rows_validated += 1
                visit_row.save()
            except Exception, e:
                logger.exception(e)
                visit_row.state = 'error'
                visit_row.error_message = e.message
                rows_failed += 1
                visit_row.save()
                continue

        return rows_validated, rows_failed

    def process(self):
        from cephia.models import VisitRow, Visit, Study
        
        rows_inserted = 0
        rows_failed = 0

        for visit_row in VisitRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            try:
                with transaction.atomic():
                    self.register_dates(visit_row.model_to_dict())

                    visit = Visit.objects.create(
                        subject_label = visit_row.subject_label,
                        visit_date = self.registered_dates.get('visitdate', None),
                        visit_hivstatus = visit_row.visit_hivstatus,
                        source_study = Study.objects.get(name=visit_row.source_study),
                        cd4_count = visit_row.cd4_count or None,
                        vl_reported = visit_row.vl or None,
                        scopevisit_ec = self.get_bool(visit_row.scopevisit_ec) or False,
                        pregnant = self.get_bool(visit_row.pregnant),
                        hepatitis = self.get_bool(visit_row.hepatitis),
                        artificial = self.get_bool(visit_row.artificial)
                    )

                    visit_row.state = 'processed'
                    visit_row.date_processed = timezone.now()
                    visit_row.error_message = ''
                    visit_row.visit = visit
                    visit_row.save()

                    rows_inserted += 1

            except Exception, e:
                logger.exception(e)
                visit_row.state = 'error'
                visit_row.error_message = e.message
                visit_row.save()
                rows_failed += 1
                continue
                    
        return rows_inserted, rows_failed
