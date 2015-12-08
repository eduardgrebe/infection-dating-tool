from file_handler import FileHandler
from handler_imports import *
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)


class SubjectFileHandler(FileHandler):

    def __init__(self, upload_file, *args, **kwargs):
        super(SubjectFileHandler, self).__init__(upload_file)

        self.registered_columns = ['subject_label',
                                   'source_study',
                                   'cohort_entry_date_yyyy',
                                   'cohort_entry_date_mm',
                                   'cohort_entry_date_dd',
                                   'country',
                                   'cohort_entry_hiv_status',
                                   'last_negative_date_yyyy',
                                   'last_negative_date_mm',
                                   'last_negative_date_dd',
                                   'first_positive_date_yyyy',
                                   'first_positive_date_mm',
                                   'first_positive_date_dd',
                                   'edsc_reported_yyyy',
                                   'edsc_reported_mm',
                                   'edsc_reported_dd',
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


    def parse(self):
        from cephia.models import SubjectRow
        
        rows_inserted = 0
        rows_failed = 0
        
        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    if not row_dict:
                        continue
                    
                    if row_dict.get('id', None):
                        try:
                            subject_row = SubjectRow.objects.get(pk=row_dict['id'], state__in=['error', 'pending', 'validated', 'imported'])
                        except SubjectRow.DoesNotExist, e:
                            continue 
                    else:
                        subject_row = SubjectRow.objects.create(subject_label=row_dict['subject_label'], fileinfo=self.upload_file)

                    subject_row.subject_label = row_dict['subject_label']
                    subject_row.source_study = row_dict['source_study']
                    subject_row.cohort_entry_date_yyyy = row_dict['cohort_entry_date_yyyy']
                    subject_row.cohort_entry_date_mm = row_dict['cohort_entry_date_mm']
                    subject_row.cohort_entry_date_dd = row_dict['cohort_entry_date_dd']
                    subject_row.country = row_dict['country']
                    subject_row.cohort_entry_hiv_status = row_dict['cohort_entry_hiv_status']
                    subject_row.last_negative_date_yyyy = row_dict['last_negative_date_yyyy']
                    subject_row.last_negative_date_mm = row_dict['last_negative_date_mm']
                    subject_row.last_negative_date_dd = row_dict['last_negative_date_dd']
                    subject_row.first_positive_date_yyyy = row_dict['first_positive_date_yyyy']
                    subject_row.first_positive_date_mm = row_dict['first_positive_date_mm']
                    subject_row.first_positive_date_dd = row_dict['first_positive_date_dd']
                    subject_row.edsc_reported_yyyy = row_dict['edsc_reported_yyyy']
                    subject_row.edsc_reported_mm = row_dict['edsc_reported_mm']
                    subject_row.edsc_reported_dd = row_dict['edsc_reported_dd']
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
                    subject_row.fileinfo=self.upload_file
                    subject_row.state = 'pending'
                    subject_row.error_message = ''
                    subject_row.save()

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1

        return rows_inserted, rows_failed

    def validate(self):
        from cephia.models import Ethnicity, Subtype, Country, Subject, SubjectRow

        rows_validated = 0
        rows_failed = 0
        default_less_date = datetime.now().date() - relativedelta(years=75)
        default_more_date = datetime.now().date() + relativedelta(years=75)
        pending_rows = SubjectRow.objects.filter(fileinfo=self.upload_file, state='pending')

        for subject_row in pending_rows:
            try:
                error_msg = ''
                self.register_dates(subject_row.model_to_dict())

                for key, value in self.registered_dates.iteritems():
                    if self.registered_dates.has_key('date_of_birth'):
                        if self.registered_dates['date_of_birth'] > value:
                            error_msg += 'Date of birth cannot be after %s.\n' % key

                    if self.registered_dates.has_key('date_of_death'):
                        if self.registered_dates['date_of_death'] < value:
                            error_msg += 'Date of death cannot be before %s.\n' % key

                if not self.registered_dates.get('last_negative_date', default_less_date) < self.registered_dates.get('first_positive_date', default_more_date):
                    error_msg += 'last_negative_date must be before first_positive_date.\n'

                # if not self.registered_dates.get('art_initiation_date', default_more_date) >= self.registered_dates.get('first_positive_date', default_less_date):
                #     error_msg += 'art_initiation_date must not be before first_positive_date.\n'

                if not self.registered_dates.get('art_interruption_date', default_more_date) > self.registered_dates.get('art_initiation_date', default_less_date):
                    error_msg += 'art_interruption_date must be after art_initiation_date.\n'
        
                if not self.registered_dates.get('art_resumption_date', default_more_date) > self.registered_dates.get('art_interruption_date', default_less_date):
                    error_msg += 'art_resumption_date must be after art_interruption_date.\n'

                if not self.registered_dates.get('aids_diagnosis_date', default_more_date) >= self.registered_dates.get('first_positive_date', default_less_date):
                    error_msg += 'aids_diagnosis_date cannot be before first_positive_date.\n'

                exists = Subject.objects.filter(subject_label=subject_row.subject_label).exists()
                if exists:
                    error_msg += "Subject already exists.\n"

                try:
                    if subject_row.population_group:
                        Ethnicity.objects.get(name=subject_row.population_group)
                except Ethnicity.DoesNotExist:
                    error_msg += "Reported ethnicity not in ethnicities table.\n"

                try:
                    Subtype.objects.get_or_create(name=subject_row.subtype)
                except Subtype.DoesNotExist:
                    error_msg += "Reported subtype not in subtypes table.\n"
            
                try:
                    Country.objects.get(code=subject_row.country)
                except Country.DoesNotExist:
                    error_msg += "Reported country not in countries table.\n"

                if error_msg:
                    raise Exception(error_msg)
                
                subject_row.state = 'validated'
                subject_row.error_message = ''
                rows_validated += 1
                subject_row.save()
            except Exception, e:
                logger.exception(e)
                subject_row.state = 'error'
                subject_row.error_message = e.message
                subject_row.save()
                rows_failed += 1
                continue
            
        return rows_validated, rows_failed
        
    def process(self):
        from cephia.models import Ethnicity, Subtype, Country, Subject, SubjectRow, Study
        
        rows_inserted = 0
        rows_failed = 0

        for subject_row in SubjectRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            try:
                with transaction.atomic():
                    self.register_dates(subject_row.model_to_dict())

                    try:
                        ethnicity = Ethnicity.objects.get(name=subject_row.population_group)
                    except Ethnicity.DoesNotExist:
                        ethnicity = None
                    
                    subject = Subject.objects.create(subject_label=subject_row.subject_label,
                                                     source_study=Study.objects.get(name=subject_row.source_study),
                                                     cohort_entry_date = self.registered_dates.get('cohort_entry_date', None),
                                                     cohort_entry_hiv_status = subject_row.cohort_entry_hiv_status,
                                                     country = Country.objects.get(code=subject_row.country),
                                                     last_negative_date = self.registered_dates.get('last_negative_date', None),
                                                     first_positive_date = self.registered_dates.get('first_positive_date', None),
                                                     ars_onset_date = self.registered_dates.get('ars_onset_date', None),
                                                     fiebig_stage_at_firstpos = subject_row.fiebig_stage_at_firstpos,
                                                     date_of_birth = self.registered_dates.get('date_of_birth', None),
                                                     date_of_death = self.registered_dates.get('date_of_death', None),
                                                     sex = subject_row.sex,
                                                     transgender = self.get_bool(subject_row.transgender),
                                                     population_group = ethnicity,
                                                     risk_sex_with_men = self.get_bool(subject_row.risk_sex_with_men),
                                                     risk_sex_with_women = self.get_bool(subject_row.risk_sex_with_women),
                                                     risk_idu = self.get_bool(subject_row.risk_idu),
                                                     subtype_confirmed = self.get_bool(subject_row.subtype_confirmed),
                                                     subtype = Subtype.objects.get(name=subject_row.subtype),
                                                     edsc_reported = self.registered_dates.get('edsc_reported', None),
                                                     art_initiation_date = self.registered_dates.get('art_initiation_date', None),
                                                     aids_diagnosis_date = self.registered_dates.get('aids_diagnosis_date', None),
                                                     art_interruption_date = self.registered_dates.get('art_interruption_date', None),
                                                     art_resumption_date = self.registered_dates.get('art_resumption_date', None))

                    subject_row.state = 'processed'
                    subject_row.error_message = ''
                    subject_row.date_processed = timezone.now()
                    subject_row.subject = subject
                    rows_inserted += 1
                    subject_row.save()
            except Exception, e:
                logger.exception(e)
                subject_row.state = 'error'
                subject_row.error_message = e.message
                subject_row.save()
                rows_failed += 1
                continue
                    
        return rows_inserted, rows_failed
