from file_handler import FileHandler
from handler_imports import *

class VisitFileHandler(FileHandler):
    visit_file = None
    
    def __init__(self, visit_file):
        super(VisitFileHandler, self).__init__()
        self.visit_file = visit_file
        self.excel_visit_file = ExcelHelper(f=visit_file.data_file.url)

        self.registered_columns = ['subject_label',
                                   'visitdate_yyyy',
                                   'visitdate_mm',
                                   'visitdate_dd',
                                   'source_study',
                                   'cd4_count',
                                   'vl',
                                   'scopevisit_ec',
                                   'pregnant',
                                   'hepatitis']

        self.existing_columns = self.excel_visit_file.read_header()

    def parse(self):
        from cephia.models import VisitRow
        
        header = self.excel_visit_file.read_header()
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.excel_visit_file.nrows):
            try:
                if row_num >= 1:
                    row = self.excel_visit_file.read_row(row_num)
                    row_dict = dict(zip(header, row))
                    
                    visit_row = VisitRow.objects.create(subject_label=row_dict['subject_label'])

                    visit_row.subject_label = row_dict['subject_label']
                    visit_row.visitdate_yyyy = row_dict['visitdate_yyyy']
                    visit_row.visitdate_mm = row_dict['visitdate_mm']
                    visit_row.visitdate_yyyy = row_dict['visitdate_mm']
                    visit_row.source_study = row_dict['source_study']
                    visit_row.cd4_count = row_dict['visit_cd4']
                    visit_row.vl = row_dict['vl']
                    visit_row.sopevisit_ec = row_dict['scopevisit_ec']
                    visit_row.pregnant = row_dict['pregnant']
                    visit_row.hepatitis = row_dict['hepatitis']

                    visit_row.fileinfo = self.visit_file
                    visit_row.state = 'pending'
                    visit_row.save()

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.visit_file.message = "row " + str(row_num) + ": " + e.message
                self.visit_file.save()
                return 0, 1

        return rows_inserted, rows_failed

    def validate(self, row_dict):
        self.register_dates()

        if not self.registered_dates['visit_date'] > self.registered_dates['cohort_entry_date']:
            raise Exception('visit_date must be greater than cohort_entry_date')

        if not self.registered_dates['visit_date'] < datetime.now().date():
            raise Exception('visit_date must be smaller than today')

        if row_dict['cohort_entry_hiv_status'] == 'P' and row_dict['visit_hivstatus'] != 'P':
            raise Exception('Visits HIV status cannot become "negative" if it was initially "positive"')

        if row_dict['scope_visit_ec'] and row_dict['source_study'] != 'SCOPE':
            raise Exception('scope_visit_ec must be null if source study is not "SCOPE"')

        first_visit = Visit.objects.filter(subject_label=row_dict['subject_label']).values('study__name').order_by('visit_date').first()
        if first_visit.name != row_dict['source_study']:
            raise Exception('source_study does not match other visits for the patient')

        subject_sex = Subject.objects.filter(subject_label=row_dict['subject_label']).values('sex')
        if row_dict['pregnant'] == 'Y' and subject_sex == 'M':
            raise Exception('Male subjects cannot be marked as pregnant')
        
        exists = Visit.objects.filter(patient_label=visit_row.patient_label, visit_date=self.get_date(visit_row.visit_date)).exists()
        if exists:
            raise Exception("Visit already exists")

        try:
            study = Study.objects.get(name=visit_row.source)
        except Study.DoesNotExist:
            raise Exception("Study does not exist")

    def process(self):
        from cephia.models import VisitRow, Visit, Study
        
        rows_inserted = 0
        rows_failed = 0

        for visit_row in VisitRow.objects.filter(fileinfo=self.visit_file, state='validated'):
            try:
                with transaction.atomic():
                    if visit_row.cd4_count:
                        cd4 = visit_row.cd4_count
                    else:
                        cd4 = None
    
                    if visit_row.vl:
                        vl = visit_row.vl
                    else:
                        vl = None

                    Visit.objects.create(visit_date = self.get_date(visit_row.visit_date),
                                         status = visit_row.status,
                                         study = study,
                                         visit_cd4 = cd4,
                                         visit_vl = vl,
                                         scope_visit_ec = visit_row.scope_visit_ec,
                                         visit_pregnant = self.get_bool(visit_row.visit_pregnant),
                                         visit_hepatitis = self.get_bool(visit_row.visit_hepatitis),
                                         patient_label = visit_row.patient_label)

                    visit_row.state = 'processed'
                    visit_row.date_processed = timezone.now()
                    visit_row.error_message = ''
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
