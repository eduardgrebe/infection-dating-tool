from file_handler import FileHandler
from handler_imports import *


class SubjectFileHandler(FileHandler):
    subject_file = None

    def __init__(self, subject_file, *args, **kwargs):
        super(SubjectFileHandler, self).__init__()
        self.subject_file = subject_file
        self.excel_subject_file = ExcelHelper(f=subject_file.data_file.url)

        self.registered_columns = ['subject_label',
                                   'source_study',
                                   'cohort_entry_date_yyyy',
                                   'cohort_entry_date_mm',
                                   'cohort_entry_date_dd',
                                   'country',
                                   'last_negative_date_yyyy',
                                   'last_negative_date_mm',
                                   'last_negative_date_dd',
                                   'first_positive_date_yyyy',
                                   'first_positive_date_mm',
                                   'first_positive_date_dd',
                                   'fiebig_stage_at_firstpos',
                                   'ars_onset_date_yyyy',
                                   'ars_onset_date_mm',
                                   'ars_onset_date_dd',
                                   'date_of_birth_yyyy',
                                   'date_of_birth_mm',
                                   'date_of_birth_dd',
                                   'sex',
                                   'transgender',
                                   'population_group',
                                   'risk_sex_with_men',
                                   'risk_sex_with_women',
                                   'risk_idu',
                                   'subtype',
                                   'subtype_confirmed',
                                   'aids_diagnosis_date_yyyy',
                                   'aids_diagnosis_date_mm',
                                   'aids_diagnosis_date_dd',
                                   'art_initiation_date_yyyy',
                                   'art_initiation_date_mm',
                                   'art_initiation_date_dd',
                                   'art_interruption_date_yyyy',
                                   'art_interruption_date_mm',
                                   'art_interruption_date_dd',
                                   'art_resumption_date_yyyy',
                                   'art_resumption_date_mm',
                                   'art_resumption_date_dd']

        self.existing_columns = self.excel_subject_file.read_header()


    def parse(self):
        from cephia.models import SubjectRow
        
        header = self.excel_subject_file.read_header()
        rows_inserted = 0
        rows_failed = 0
        
        for row_num in range(self.excel_subject_file.nrows):
            try:
                if row_num >= 1:
                    row = self.excel_subject_file.read_row(row_num)
                    row_dict = dict(zip(header, row))

                    subject_row = SubjectRow.objects.create(subject_label=row_dict['subject_label'], fileinfo=self.subject_file)

                    subject_row.subject_label = row_dict['subject_label']
                    subject_row.source_study = row_dict['source_study']
                    subject_row.cohort_entry_date_yyyy = row_dict['cohort_entry_date_yyyy']
                    subject_row.cohort_entry_date_mm = row_dict['cohort_entry_date_mm']
                    subject_row.cohort_entry_date_dd = row_dict['cohort_entry_date_dd']
                    subject_row.country = row_dict['country']
                    subject_row.last_negative_date_yyyy = row_dict['last_negative_date_yyyy']
                    subject_row.last_negative_date_mm = row_dict['last_negative_date_mm']
                    subject_row.last_negative_date_dd = row_dict['last_negative_date_dd']
                    subject_row.first_positive_date_yyyy = row_dict['first_positive_date_yyyy']
                    subject_row.first_positive_date_mm = row_dict['first_positive_date_mm']
                    subject_row.first_positive_date_dd = row_dict['first_positive_date_dd']
                    subject_row.fiebig_stage_at_firstpos = row_dict['fiebig_stage_at_firstpos']
                    subject_row.ars_onset_date_yyyy = row_dict['ars_onset_date_yyyy']
                    subject_row.ars_onset_date_mm = row_dict['ars_onset_date_mm']
                    subject_row.ars_onset_date_dd = row_dict['ars_onset_date_dd']
                    subject_row.date_of_birth_yyyy = row_dict['date_of_birth_yyyy']
                    subject_row.date_of_birth_mm = row_dict['date_of_birth_mm']
                    subject_row.date_of_birth_dd = row_dict['date_of_birth_dd']
                    subject_row.sex = row_dict['sex']
                    subject_row.transgender = row_dict['transgender']
                    subject_row.population_group = row_dict['population_group']
                    subject_row.risk_sex_with_men = row_dict['risk_sex_with_men']
                    subject_row.risk_sex_with_women = row_dict['risk_sex_with_women']
                    subject_row.risk_idu = row_dict['risk_idu']
                    subject_row.subtype = row_dict['subtype']
                    subject_row.subtype_confirmed = row_dict['subtype_confirmed']
                    subject_row.aids_diagnosis_date_yyyy = row_dict['aids_diagnosis_date_yyyy']
                    subject_row.aids_diagnosis_date_mm = row_dict['aids_diagnosis_date_mm']
                    subject_row.aids_diagnosis_date_dd = row_dict['aids_diagnosis_date_dd']
                    subject_row.art_initiation_date_yyyy = row_dict['art_initiation_date_yyyy']
                    subject_row.art_initiation_date_mm = row_dict['art_initiation_date_mm']
                    subject_row.art_initiation_date_dd = row_dict['art_initiation_date_dd']
                    subject_row.art_interruption_date_yyyy = row_dict['art_interruption_date_yyyy']
                    subject_row.art_interruption_date_mm = row_dict['art_interruption_date_mm']
                    subject_row.art_interruption_date_dd = row_dict['art_interruption_date_dd']
                    subject_row.art_resumption_date_yyyy = row_dict['art_resumption_date_yyyy']
                    subject_row.art_resumption_date_mm = row_dict['art_resumption_date_mm']
                    subject_row.art_resumption_date_dd = row_dict['art_resumption_date_dd']
                    subject_row.state = 'pending'
                    subject_row.save()

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.subject_file.message = "row " + str(row_num) + ": " + e.message
                self.subject_file.save()
                return 0, 1

        return rows_inserted, rows_failed

    def validate(self):
        from cephia.models import Ethnicity, Subtype, Country, Subject, SubjectRow
        
        for subject_row in SubjectRow.objects.filter(fileinfo=self.subject_file, state='pending'):
            try:
                self.register_dates(subject_row.model_to_dict())
            
                for key, value in self.registered_dates.iteritems():
                    if self.registered_dates['date_of_birth'] > value:
                        raise Exception('Date of birth cannot be greater than %s' % key)

                    if self.registered_dates['date_of_death'] < value:
                        raise Exception('Date of death cannot be smaller than %s' % key)

                if not self.registered_dates['last_negative_date'] < self.registered_dates['first_positive_date']:
                    raise Exception('last_negative_date must be smaller than first_positive_date')

                if not self.registered_dates['ars_onset_date'] < self.registered_dates['first_positive_date']:
                    raise Exception('ars_onset_date must be smaller than first_positive_date')

                if not self.registered_dates['art_initiation_date'] > self.registered_dates['first_positive_date']:
                    raise Exception('art_initiation_date must be larger than first_positive_date')

                if not self.registered_dates['art_interruption_date'] > self.registered_dates['art_initiation_date']:
                    raise Exception('art_interruption_date must be greater than art_initiation_date')
        
                if not self.registered_dates['art_resumption_date'] > self.registered_dates['art_interruption_date']:
                    raise Exception('ars_resumption_date must be greater than art_interruption_date')

                if not self.registered_dates['aids_diagnosis_date'] > self.registered_dates['first_positive_date']:
                    raise Exception('ars_onset_date must be smaller than first_positive_date')

                exists = Subject.objects.filter(subject_label=subject_row.subject_label).exists()
                if exists:
                    raise Exception("Subject already exists")

                try:
                    if subject_row.ethnicity:
                        Ethnicity.objects.get(name=subject_row.ethnicity)
                except Ethnicity.DoesNotExist:
                    raise Exception("Ethnicity does not exist")

                try:
                    Subtype.objects.get(name=subject_row.subtype)
                except Subtype.DoesNotExist:
                    raise Exception("Subtype does not exist")
            
                try:
                    country = Country.objects.get(code=subject_row.country)
                except Country.DoesNotExist:
                    raise Exception("Country does not exist")
                
                subject_row.state = 'validated'
                subject_row.error_message = ''
                #subject_row.date_processed = timezone.now()
                subject_row.save()
            except Exception, e:
                #logger.exception(e)
                import pdb; pdb.set_trace()
                subject_row.state = 'error'
                subject_row.error_message = e.message
                subject_row.save()
                continue
        
    def process(self):
        from cephia.models import Ethnicity, Subtype, Country, Subject, SubjectRow
        
        rows_inserted = 0
        rows_failed = 0

        for subject_row in SubjectRow.objects.filter(fileinfo=self.subject_file, state='validated'):
            try:
                with transaction.atomic():
                    Subject.objects.create(patient_label=subject_row.patient_label,
                                           entry_date = self.get_date(subject_row.entry_date),
                                           entry_status = subject_row.entry_status,
                                           country = country,
                                           last_negative_date = self.get_date(subject_row.last_negative_date),
                                           last_positive_date = self.get_date(subject_row.last_positive_date),
                                           ars_onset = self.get_date(subject_row.ars_onset),
                                           fiebig = subject_row.fiebig,
                                           dob = self.get_year(subject_row.dob),
                                           gender = subject_row.gender,
                                           ethnicity = ethnicity,
                                           sex_with_men = self.get_bool(subject_row.sex_with_men),
                                           sex_with_women = self.get_bool(subject_row.sex_with_women),
                                           iv_drug_user = self.get_bool(subject_row.iv_drug_user),
                                           subtype_confirmed = self.get_bool(subject_row.subtype_confirmed),
                                           subtype = subtype,
                                           anti_retroviral_initiation_date = self.get_date(subject_row.anti_retroviral_initiation_date),
                                           aids_diagnosis_date = self.get_date(subject_row.aids_diagnosis_date),
                                           treatment_interruption_date = self.get_date(subject_row.treatment_interruption_date),
                                           treatment_resumption_date = self.get_date(subject_row.treatment_resumption_date))

                    subject_row.state = 'processed'
                    subject_row.error_message = ''
                    subject_row.date_processed = timezone.now()
                    rows_inserted += 1
                    subject_row.save()
            except Exception, e:
                #logger.exception(e)
                import pdb; pdb.set_trace()
                subject_row.state = 'error'
                subject_row.error_message = e.message
                subject_row.save()
                rows_failed += 1
                continue
                    
        return rows_inserted, rows_failed
