from excel_helper import ExcelHelper
from models import SubjectRow, Subject
from datetime import datetime


class SubjectFileHandler(object):
    subject_file = None

    def __init__(self, subject_file):
        self.subject_file = subject_file
        self.excel_subject_file = ExcelHelper(f=subject_file.data_file.url)

    def parse(self):
        for row_num in range(self.excel_subject_file.nrows):
            row = self.excel_subject_file.read_row(row_num)

            try:
                if row_num > 1:
                    subject_row, created = SubjectRow.objects.get_or_create(patient_label=row[0], fileinfo=self.subject_file)
                    
                    subject_row.patient_label = row[0]
                    subject_row.entry_date = row[1]
                    subject_row.entry_status = row[2]
                    subject_row.country = row[3]
                    subject_row.last_negative_date = row[4]
                    subject_row.last_positive_date = row[5]
                    subject_row.ars_onset = row[6]
                    subject_row.fiebig = row[7]
                    subject_row.dob = row[8]
                    subject_row.gender = row[9]
                    subject_row.ethnicity = row[10]
                    subject_row.sex_with_men = row[11]
                    subject_row.sex_with_women = row[12]
                    subject_row.iv_drug_user = row[13]
                    subject_row.subtype_confirmed = row[14]
                    subject_row.subtype = row[15]
                    subject_row.anti_retroviral_initiation_date = row[16]
                    subject_row.aids_diagnosis_date = row[17]
                    subject_row.treatment_interruption_date = row[18]
                    subject_row.treatment_resumption_date = row[19]
                    subject_row.fileinfo = self.subject_file
                    subject_row.save()
            except Exception, e:
                logger.exception(e)
                return False

        return True


    def copy_to_subject_table(self):
        
        for subject_row in SubjectRow.objects.filter(state='pending'):
            subject = Subject.objects.get_or_create(patient_label=subject_row.patient_label)

            try:
                subject.patient_label = subject_row.patient_label
                subject.entry_date = subject_row.entry_date
                subject.entry_status = subject_row.entry_status
                subject.country = subject_row.country
                subject.last_negative_date = subject_row.last_negative_date
                subject.last_positive_date = subject_row.last_positive_date
                subject.ars_onset = subject_row.ars_onset
                subject.fiebig = subject_row.fiebig
                subject.dob = subject_row.dob
                subject.gender = subject_row.gender
                subject.ethnicity = subject_row.ethnicity
                subject.sex_with_men = subject_row.sex_with_men
                subject.sex_with_women = subject_row.sex_with_women
                subject.iv_drug_user = subject_row.iv_drug_user
                subject.subtype_confirmed = subject_row.subtype_confirmed
                subject.subtype = subject_row.subtype
                subject.anti_retroviral_initiation_date = subject_row.anti_retroviral_initiation_date
                subject.aids_diagnosis_date = subject_row.aids_diagnosis_date
                subject.treatment_interruption_date = subject_row.treatment_interruption_date
                subject.treatment_resumption_date = subject_row.treatment_resumption_date

                subject.state = 'processed'
                subject.date_processed = datetime.now()

            except Exception, e:
                subject_row.state = 'error'
                subject_row.message = e
                subject_row.save()
                continue
                

                

