from excel_helper import ExcelHelper
from models import SubjectRow, VisitRow, Subject, Ethnicity, Country, Subtype, Visit, Source, TransferInRow, Specimen, SpecimenType
from datetime import datetime
from django.db import transaction
import logging

class FileHandler(object):
    logger = logging.getLogger(__name__)

    def get_date(self, date_string):
        if date_string:
            return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date()
        else:
            return None

    def get_bool(self, bool_string):
        if bool_string:
            if bool_string == '0':
                return False
            elif bool_string == '1':
                return True
        else:
            return False
        
class SubjectFileHandler(FileHandler):
    subject_file = None
    
    def __init__(self, subject_file):
        self.subject_file = subject_file
        self.excel_subject_file = ExcelHelper(f=subject_file.data_file.url)

    def parse(self):
        header = self.excel_subject_file.read_header()
        date_cols = [1,4,5,6,8,16,17,18,19]
        rows_inserted = 0
        rows_failed = 0
        
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

                    rows_inserted = rows_inserted + 1
            except Exception, e:
                rows_failed = rows_failed + 1
                continue

        return rows_inserted, rows_failed


    def process(self):
        rows_inserted = 0
        rows_failed = 0

        for subject_row in SubjectRow.objects.filter(fileinfo=self.subject_file, state__in=['pending', 'error']):
            try:
                with transaction.atomic():
                    if subject_row.ethnicity:
                        ethnicity = subject_row.ethnicity
                    else:
                        ethnicity = 'Unknown'

                    ethnicity_object, ethnicity_created = Ethnicity.objects.get_or_create(name=ethnicity)
                    subtype, subtype_created = Subtype.objects.get_or_create(name=subject_row.subtype)
                    country = Country.objects.get(code=subject_row.country)

                    subject = Subject.objects.get_or_create(patient_label=subject_row.patient_label,
                                                    entry_date = self.get_date(subject_row.entry_date),
                                                    entry_status = subject_row.entry_status,
                                                    country = country,
                                                    last_negative_date = self.get_date(subject_row.last_negative_date),
                                                    last_positive_date = self.get_date(subject_row.last_positive_date),
                                                    ars_onset = self.get_date(subject_row.ars_onset),
                                                    fiebig = subject_row.fiebig,
                                                    dob = self.get_date(subject_row.dob),
                                                    gender = subject_row.gender,
                                                    ethnicity = ethnicity_object,
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
                    subject_row.date_processed = datetime.now()
                    rows_inserted = rows_inserted + 1
                    subject_row.save()
            except Exception, e:
                subject_row.state = 'error'
                subject_row.error_message = e.message
                subject_row.save()
                rows_failed = rows_failed + 1
                continue
                
        return rows_inserted, rows_failed


class VisitFileHandler(FileHandler):
    visit_file = None
    
    def __init__(self, visit_file):
        self.visit_file = visit_file
        self.excel_visit_file = ExcelHelper(f=visit_file.data_file.url)

    def parse(self):
        header = self.excel_visit_file.read_header()
        date_cols = [1]
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.excel_visit_file.nrows):
            try:
                if row_num >= 1:
                    row = self.excel_visit_file.read_row(row_num, date_cols)
                    row_dict = dict(zip(header, row))

                    visit_row, created = VisitRow.objects.get_or_create(visit_label=row_dict['visit_pt_id'],
                                                                        visit_date=row_dict['visit_date'],
                                                                        fileinfo=self.visit_file)

                    visit_row.visit_label = row_dict['visit_pt_id']
                    visit_row.visit_date = row_dict['visit_date']
                    visit_row.status = row_dict['visit_status']
                    visit_row.source = row_dict['visit_source']
                    visit_row.visit_cd4 = row_dict['visit_cd4']
                    visit_row.visit_vl = row_dict['visit_vl']
                    visit_row.sopevisit_ec = row_dict['scopevisit_ec']
                    visit_row.visit_pregnant = row_dict['visit_pregnant']
                    visit_row.visit_hepatitis = row_dict['visit_hepatitis']

                    visit_row.fileinfo = self.visit_file
                    visit_row.state = 'pending'
                    visit_row.save()

                    rows_inserted = rows_inserted + 1
            except Exception, e:
                rows_failed = rows_failed + 1
                continue

        return rows_inserted, rows_failed


    def process(self):
        rows_inserted = 0
        rows_failed = 0

        for visit_row in VisitRow.objects.filter(fileinfo=self.visit_file, state__in=['pending', 'error']):
            try:
                with transaction.atomic():
                    source,  source_create = Source.objects.get_or_create(name=visit_row.source)

                    if not visit_row.visit_cd4:
                        cd4 = 0
                    else:
                        cd4 = visit_row.visit_cd4

                    visit = Visit.objects.create(visit_date = self.get_date(visit_row.visit_date),
                                                 status = visit_row.status,
                                                 source = source,
                                                 visit_cd4 = cd4,
                                                 visit_vl = visit_row.visit_vl,
                                                 scope_visit_ec = visit_row.scope_visit_ec,
                                                 visit_pregnant = self.get_bool(visit_row.visit_pregnant),
                                                 visit_hepatitis = self.get_bool(visit_row.visit_hepatitis),
                                                 visit_label = visit_row.visit_label)

                    visit_row.state = 'processed'
                    visit_row.date_processed = datetime.now()
                    visit_row.save()
                    rows_inserted = rows_inserted + 1
            except Exception, e:
                visit_row.state = 'error'
                visit_row.error_message = e.message
                visit_row.save()
                rows_failed = rows_failed + 1
                continue
            
        return rows_inserted, rows_failed



class TransferInFileHandler(FileHandler):
    transfer_in_file = None
    
    def __init__(self, transfer_in_file):
        self.transfer_in_file = transfer_in_file
        self.excel_transfer_in_file = ExcelHelper(f=transfer_in_file.data_file.url)

    def parse(self):
        header = self.excel_transfer_in_file.read_header()
        date_cols = [2,4]
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.excel_transfer_in_file.nrows):
            try:
                if row_num >= 1:
                    row = self.excel_transfer_in_file.read_row(row_num, date_cols)
                    row_dict = dict(zip(header, row))

                    transfer_in_row, created = TransferInRow.objects.get_or_create(specimen_label=row_dict['specimen id'],
                                                                                   patient_label=row_dict['subject_id'],
                                                                                   draw_date=row_dict['draw_date'],
                                                                                   fileinfo=self.transfer_in_file)

                    transfer_in_row.specimen_label = row_dict['specimen id']
                    transfer_in_row.patient_label = row_dict['subject_id']
                    transfer_in_row.draw_date = row_dict['draw_date']
                    transfer_in_row.num_containers = row_dict['number of containers']
                    transfer_in_row.transfer_in_date = row_dict['transfer date']
                    transfer_in_row.sites = row_dict['sites']
                    transfer_in_row.transfer_reason = row_dict['transfer reason']
                    transfer_in_row.spec_type = row_dict['spec type']
                    transfer_in_row.volume = row_dict['volume']


                    transfer_in_row.fileinfo = self.transfer_in_file
                    transfer_in_row.state = 'pending'
                    transfer_in_row.save()

                    rows_inserted = rows_inserted + 1
            except Exception, e:
                rows_failed = rows_failed + 1
                continue

        return rows_inserted, rows_failed


    def process(self):
        rows_inserted = 0
        rows_failed = 0

        for transfer_in_row in TransferInRow.objects.filter(fileinfo=self.transfer_in_file, state__in=['pending', 'error']):

            try:
                with transaction.atomic():
                    subject = Subject.objects.get(patient_label=transfer_in_row.patient_label)

                    spec_type_group = transfer_in_row.spec_type.split()
                    spec_type = SpecimenType.objects.get_or_create(spec_type=spec_type_group[0],
                                                                   spec_group=spec_type_group[1],
                                                                   name='')

                    specimen = Specimen.objects.create(label = self.get_date(transfer_in_row.specimen_label),
                                                       subject = subject,
                                                       draw_date = transfer_in_row.draw_date,
                                                       num_containers = transfer_in_row.num_containers,
                                                       transfer_in_date = transfer_in_row.transfer_in_date,
                                                       souce_study = transfer_in_row.sites,
                                                       spec_type = spec_type,
                                                       volume = transfer_in_row.volume)

                    transfer_in_row.state = 'processed'
                    transfer_in_row.date_processed = datetime.now()
                    transfer_in_row.save()

                    rows_inserted = rows_inserted + 1
            except Exception, e:
                transfer_in_row.state = 'error'
                transfer_in_row.error_message = e.message
                transfer_in_row.save()

                rows_failed = rows_failed + 1
                continue

        return rows_inserted, rows_failed
