from excel_helper import ExcelHelper
from models import SubjectRow, Subject, Ethnicity, Country, Subtype
from datetime import datetime


class SubjectFileHandler(object):
    subject_file = None
    
    def __init__(self, subject_file):
        self.subject_file = subject_file
        self.excel_subject_file = ExcelHelper(f=subject_file.data_file.url)

    def get_date(self, date_string):
        if date_string:
            return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date()
        else:
            return None

    def get_bool(self, bool_string):
        if bool_string:
            if bool_string == '0':
                return False
            else if bool_string == '1':
                return True
        else:
            return False

    def parse(self):
        header = self.excel_subject_file.read_header()
        date_cols = [1,4,5,8,16,17,18,19]

        for row_num in range(self.excel_subject_file.nrows):
            try:
                if row_num >= 1:
                    row = self.excel_subject_file.read_row(row_num, date_cols)
                    row_dict = dict(zip(header, row))
                    
                    subject_row, created = SubjectRow.objects.get_or_create(patient_label=row_dict['pt_id'], fileinfo=self.subject_file)

                    subject_row.patient_label = row_dict['pt_id']
                    subject_row.entry_date = row_dict['pt_entrydt']
                    subject_row.entry_status = row_dict['pt_entrystat']
                    subject_row.country = row_dict['pt_country']
                    subject_row.last_negative_date = row_dict['pt_lastnegdate']
                    subject_row.last_positive_date = row_dict['pt_firstpozdate']
                    subject_row.ars_onset = row_dict['pt_arsonset']
                    subject_row.fiebig = row_dict['pt_fiebig']
                    subject_row.dob = row_dict['pt_yob']
                    subject_row.gender = row_dict['pt_sex']
                    subject_row.ethnicity = row_dict['pt_ethnicity']
                    subject_row.sex_with_men = row_dict['pt_sexwithmen']
                    subject_row.sex_with_women = row_dict['pt_sexwithwomen']
                    subject_row.iv_drug_user = row_dict['pt_ivdu']
                    subject_row.subtype_confirmed = row_dict['pt_subconf']
                    subject_row.subtype = row_dict['pt_subtype']
                    subject_row.anti_retroviral_initiation_date = row_dict['pt_arvdate']
                    subject_row.aids_diagnosis_date = row_dict['pt_aidsdx']
                    subject_row.treatment_interruption_date = row_dict['pt_txintdate']
                    subject_row.treatment_resumption_date = row_dict['pt_txresdate']
                    subject_row.fileinfo = self.subject_file
                    subject_row.state = 'pending'
                    subject_row.save()
            except Exception, e:
                logger.exception(e)
                return False

        return True


    def process(self):
        for subject_row in SubjectRow.objects.filter(fileinfo=self.subject_file, state__in=['pending', 'error']):
            try:
                ethnicity, ethnicity_created = Ethnicity.objects.get_or_create(name=subject_row.ethnicity)
                subtype, subtype_created = Subtype.objects.get_or_create(name=subject_row.subtype)
                country = Country.objects.get(code=subject_row.country)
                
                #process dates correctly

                if subject_row.last_negative_date:
                    lnd = datetime.strptime(subject_row.last_negative_date, "%Y-%m-%d %H:%M:%S").date()
                else:
                    lnd = None

                if subject_row.last_positive_date:
                    lpd = datetime.strptime(subject_row.last_positive_date, "%Y-%m-%d %H:%M:%S").date()
                else:
                    lpd = None

                if subject_row.dob:
                    dob = datetime.strptime(subject_row.dob, "%Y-%m-%d %H:%M:%S").date()
                else:
                    dob = None

                if subject_row.ars_onset:
                    ars = datetime.strptime(subject_row.ars_onset, "%Y-%m-%d %H:%M:%S").date()
                else:
                    ars = None
                    
                if subject_row.anti_retroviral_initiation_date:
                    arid = datetime.strptime(subject_row.anti_retroviral_initiation_date, "%Y-%m-%d %H:%M:%S").date()
                else:
                    arid = None

                if subject_row.aids_diagnosis_date:
                    add = datetime.strptime(subject_row.aids_diagnosis_date, "%Y-%m-%d %H:%M:%S").date()
                else:
                    add = None

                if subject_row.treatment_interruption_date:
                    tid = datetime.strptime(subject_row.treatment_interruption_date, "%Y-%m-%d %H:%M:%S").date()
                else:
                    tid = None

                if subject_row.treatment_resumption_date:
                    tsd = datetime.strptime(subject_row.treatment_resumption_date, "%Y-%m-%d %H:%M:%S").date()
                else:
                    tsd = None
                #

                subject, subject_created = Subject.objects.get_or_create(patient_label=subject_row.patient_label,
                                                        entry_date = self.get_date(subject_row.entry_date),
                                                        entry_status = subject_row.entry_status,
                                                        country = country,
                                                        last_negative_date = lnd,
                                                        last_positive_date = lpd,
                                                        ars_onset = ars,
                                                        fiebig = subject_row.fiebig,
                                                        dob = dob,
                                                        gender = subject_row.gender,
                                                        ethnicity = ethnicity,
                                                        sex_with_men = self.get_bool(subject_row.sex_with_men),
                                                        sex_with_women = self.get_bool(subject_row.sex_with_women),
                                                        iv_drug_user = self.get_bool(subject_row.iv_drug_user),
                                                        subtype_confirmed = self.get_bool(subject_row.subtype_confirmed),
                                                        subtype = subtype,
                                                        anti_retroviral_initiation_date = arid,
                                                        aids_diagnosis_date = add,
                                                        treatment_interruption_date = tid,
                                                        treatment_resumption_date = tsd)

                if subject_created:
                    subject_row.state = 'processed'
                    subject_row.date_processed = datetime.now()

            except Exception, e:
                subject_row.state = 'error'
                subject_row.error_message = e.message
                subject_row.save()
                subject_row.fileinfo.state = 'error'
                subject_row.fileinfo.message = e.message
                subject_row.save()
                continue
                

                

