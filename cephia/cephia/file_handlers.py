from excel_helper import ExcelHelper
from datetime import datetime, date
from django.db import transaction
from django.utils import timezone
import logging
import xlrd

logger = logging.getLogger(__name__)

registered_file_handlers = []
def register_file_handler(file_type, cls):
    registered_file_handlers.append( (file_type, cls) )

def get_file_handler_for_type(file_type):
    for registered_file_type, registered_file_handler in registered_file_handlers:
        if file_type == registered_file_type:
            return registered_file_handler
    raise Exception("Unknown file type: %s" % file_type)



class FileHandler(object):

    def get_date(self, date_string):
        if date_string:
            return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date()
        else:
            return None

    def get_year(self, year_string):
        if year_string:
            return date(int(year_string), 1, 1)
        else:
            return None

    def get_bool(self, bool_string):
        return bool_string == '1'

    def float_to_date(self, value):
        if value:
            return datetime(*xlrd.xldate_as_tuple(float(value), 0)).date()
        else:
            return None

    def validate_file(self):
        missing_cols = list(set(self.registered_columns) - set(self.existing_columns))
        extra_cols = list(set(self.existing_columns) - set(self.registered_columns))

        if missing_cols:
            raise Exception("The following columns are missing from your file %s" % str(missing_cols))

        if extra_cols:
            return "Your file contained the following extra columns and they have been ignored %s" % str(extra_cols)
        
                
class SubjectFileHandler(FileHandler):
    subject_file = None
    
    def __init__(self, subject_file, *args, **kwargs):
        super(SubjectFileHandler, self).__init__()
        self.subject_file = subject_file
        self.excel_subject_file = ExcelHelper(f=subject_file.data_file.url)

        self.registered_columns = ['pt_id',
                                   'pt_entrydt',
                                   'pt_entrystat',
                                   'pt_country',
                                   'pt_lastnegdate',
                                   'pt_firstpozdate',
                                   'pt_arsonset',
                                   'pt_fiebig',
                                   'pt_yob',
                                   'pt_sex',
                                   'pt_ethnicity',
                                   'pt_sexwithmen',
                                   'pt_sexwithwomen',
                                   'pt_ivdu',
                                   'pt_subconf',
                                   'pt_subtype',
                                   'pt_arvdate',
                                   'pt_aidsdx',
                                   'pt_txintdate',
                                   'pt_txresdate']

        self.existing_columns = self.excel_subject_file.read_header()
        

    def parse(self):

        from models import SubjectRow
        
        header = self.excel_subject_file.read_header()
        rows_inserted = 0
        rows_failed = 0
        
        for row_num in range(self.excel_subject_file.nrows):
            try:
                if row_num >= 1:
                    row = self.excel_subject_file.read_row(row_num)
                    row_dict = dict(zip(header, row))

                    subject_row = SubjectRow.objects.create(patient_label=row_dict['pt_id'], fileinfo=self.subject_file)

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

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.subject_file.message = "row " + str(row_num) + ": " + e.message
                self.subject_file.save()
                return 0, 1

        return rows_inserted, rows_failed


    def process(self):

        from models import Ethnicity, Subtype, Country, Subject, SubjectRow
        
        rows_inserted = 0
        rows_failed = 0

        for subject_row in SubjectRow.objects.filter(fileinfo=self.subject_file, state__in=['pending']):
            try:
                with transaction.atomic():
                    try:
                        if subject_row.ethnicity:
                            ethnicity = Ethnicity.objects.get(name=subject_row.ethnicity)
                        else:
                            ethnicity = Ethnicity.objects.get(name='Unknown')
                    except Ethnicity.DoesNotExist:
                        raise Exception("Ethnicity does not exist")

                    subtype, subtype_created = Subtype.objects.get_or_create(name=subject_row.subtype)

                    try:
                        country = Country.objects.get(code=subject_row.country)
                    except Country.DoesNotExist:
                        raise Exception("Country does not exist")

                    Subject.objects.update_or_create(patient_label=subject_row.patient_label,
                                                     entry_date = self.float_to_date(subject_row.entry_date),
                                                     entry_status = subject_row.entry_status,
                                                     country = country,
                                                     last_negative_date = self.float_to_date(subject_row.last_negative_date),
                                                     last_positive_date = self.float_to_date(subject_row.last_positive_date),
                                                     ars_onset = self.float_to_date(subject_row.ars_onset),
                                                     fiebig = subject_row.fiebig,
                                                     dob = self.get_year(subject_row.dob),
                                                     gender = subject_row.gender,
                                                     ethnicity = ethnicity,
                                                     sex_with_men = self.get_bool(subject_row.sex_with_men),
                                                     sex_with_women = self.get_bool(subject_row.sex_with_women),
                                                     iv_drug_user = self.get_bool(subject_row.iv_drug_user),
                                                     subtype_confirmed = self.get_bool(subject_row.subtype_confirmed),
                                                     subtype = subtype,
                                                     anti_retroviral_initiation_date = self.float_to_date(subject_row.anti_retroviral_initiation_date),
                                                     aids_diagnosis_date = self.float_to_date(subject_row.aids_diagnosis_date),
                                                     treatment_interruption_date = self.float_to_date(subject_row.treatment_interruption_date),
                                                     treatment_resumption_date = self.float_to_date(subject_row.treatment_resumption_date))

                    subject_row.state = 'processed'
                    subject_row.error_message = ''
                    subject_row.date_processed = timezone.now()
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


class VisitFileHandler(FileHandler):
    visit_file = None
    
    def __init__(self, visit_file):
        super(VisitFileHandler, self).__init__()
        self.visit_file = visit_file
        self.excel_visit_file = ExcelHelper(f=visit_file.data_file.url)

        self.registered_columns = ['visit_pt_id',
                                   'visit_date',
                                   'visit_status',
                                   'visit_source',
                                   'visit_cd4',
                                   'visit_vl',
                                   'scopevisit_ec',
                                   'visit_pregnant',
                                   'visit_hepatitis']

        self.existing_columns = self.excel_visit_file.read_header()

    def parse(self):

        from models import VisitRow
        
        header = self.excel_visit_file.read_header()
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.excel_visit_file.nrows):
            try:
                if row_num >= 1:
                    row = self.excel_visit_file.read_row(row_num)
                    row_dict = dict(zip(header, row))

                    visit_row = VisitRow.objects.create(visit_label=row_dict['visit_pt_id'],
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

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.visit_file.message = "row " + str(row_num) + ": " + e.message
                self.visit_file.save()
                return 0, 1

        return rows_inserted, rows_failed


    def process(self):
        
        from models import VisitRow, Visit, Study
        
        rows_inserted = 0
        rows_failed = 0

        for visit_row in VisitRow.objects.filter(fileinfo=self.visit_file, state__in=['pending', 'error']):
            try:
                with transaction.atomic():
                    try:
                        study = Study.objects.get(name=visit_row.source)
                    except Study.DoesNotExist:
                        raise Exception("Study does not exist")

                    if visit_row.visit_cd4:
                        cd4 = visit_row.visit_cd4
                    else:
                        cd4 = None

                    if visit_row.visit_vl:
                        vl = visit_row.visit_vl
                    else:
                        vl = None

                    Visit.objects.update_or_create(visit_date = self.float_to_date(visit_row.visit_date),
                                                   status = visit_row.status,
                                                   study = study,
                                                   visit_cd4 = cd4,
                                                   visit_vl = vl,
                                                   scope_visit_ec = visit_row.scope_visit_ec,
                                                   visit_pregnant = self.get_bool(visit_row.visit_pregnant),
                                                   visit_hepatitis = self.get_bool(visit_row.visit_hepatitis),
                                                   visit_label = visit_row.visit_label)

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

class TransferInFileHandler(FileHandler):
    transfer_in_file = None
    
    def __init__(self, transfer_in_file):
        super(TransferInFileHandler, self).__init__()
        self.transfer_in_file = transfer_in_file
        self.excel_transfer_in_file = ExcelHelper(f=transfer_in_file.data_file.url)

        self.registered_columns = ['specimen_id',
                                   'subject_id',
                                   'draw_date',
                                   'number of containers',
                                   'transfer date',
                                   'sites',
                                   'transfer reason',
                                   'spec type',
                                   'volume']

        self.existing_columns = self.excel_transfer_in_file.read_header()

    def parse(self):
        
        from models import TransferInRow
        
        header = self.excel_transfer_in_file.read_header()
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.excel_transfer_in_file.nrows):
            try:
                if row_num >= 1:
                        
                    row = self.excel_transfer_in_file.read_row(row_num)
                    row_dict = dict(zip(header, row))
                    
                    transfer_in_row = TransferInRow.objects.create(specimen_label=row_dict['specimen id'],
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

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.transfer_in_file.message = "row " + str(row_num) + ": " + e.message
                self.transfer_in_file.save()
                return 0, 1

        return rows_inserted, rows_failed


    def process(self):
        
        from models import TransferInRow, Subject, Study, Reason, SpecimenType, Specimen, Site
        
        rows_inserted = 0
        rows_failed = 0

        for transfer_in_row in TransferInRow.objects.filter(fileinfo=self.transfer_in_file, state__in=['pending']):

            try:
                with transaction.atomic():
                    try:
                        subject = Subject.objects.get(patient_label=transfer_in_row.patient_label)
                    except Subject.DoesNotExist:
                        raise Exception("Subject does not exist")

                    try:
                        site = Site.objects.get(name=transfer_in_row.sites)
                    except Site.DoesNotExist:
                        raise Exception("Site does not exist")

                    reason, reason_created = Reason.objects.get_or_create(name=transfer_in_row.transfer_reason)

                    spec_type = SpecimenType.objects.get(spec_type=transfer_in_row.spec_type)

                    specimen, specimen_created = Specimen.objects.update_or_create(specimen_label = transfer_in_row.specimen_label,
                                                                                   subject = subject,
                                                                                   reported_draw_date = self.float_to_date(transfer_in_row.draw_date),
                                                                                   transfer_in_date = self.float_to_date(transfer_in_row.transfer_in_date),
                                                                                   source_study = site,
                                                                                   reason = reason,
                                                                                   spec_type = spec_type)

                    if transfer_in_row.num_containers:
                        specimen.num_containers = transfer_in_row.num_containers
                    else:
                        specimen.num_containers = None

                    if transfer_in_row.volume:
                        specimen.initial_claimed_volume = transfer_in_row.volume
                    else:
                        specimen.initial_claimed_volume = None

                    specimen.save()

                    transfer_in_row.state = 'processed'
                    transfer_in_row.date_processed = timezone.now()
                    transfer_in_row.save()

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                transfer_in_row.state = 'error'
                transfer_in_row.error_message = e.message
                transfer_in_row.save()

                rows_failed += 1
                continue

        return rows_inserted, rows_failed


class TransferOutFileHandler(FileHandler):
    transfer_out_file = None
    
    def __init__(self, transfer_out_file):
        super(TransferOutFileHandler, self).__init__()
        self.transfer_out_file = transfer_out_file
        self.excel_transfer_out_file = ExcelHelper(f=transfer_out_file.data_file.url)

        self.registered_columns = ['spec_id',
                                   '#_ containers',
                                   'transfer date',
                                   'to location',
                                   'reason',
                                   'spec type',
                                   'vol',
                                   'other id']

        self.existing_columns = self.excel_transfer_out_file.read_header()

    def parse(self):
        
        from models import TransferOutRow
        
        header = self.excel_transfer_out_file.read_header()
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.excel_transfer_out_file.nrows):
            try:
                if row_num >= 1:
                    row = self.excel_transfer_out_file.read_row(row_num)
                    row_dict = dict(zip(header, row))

                    transfer_out_row = TransferOutRow.objects.create(specimen_label=row_dict['spec_id'],
                                                                     num_containers=row_dict['#_ containers'],
                                                                     transfer_out_date=row_dict['transfer date'],
                                                                     to_location=row_dict['to location'],
                                                                     transfer_reason=row_dict['reason'],
                                                                     spec_type=row_dict['spec type'],
                                                                     volume=row_dict['vol'],
                                                                     other_ref=row_dict['other id'],
                                                                     fileinfo=self.transfer_out_file,
                                                                     state='pending')


                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.transfer_out_file.message = "row " + str(row_num) + ": " + e.message
                self.transfer_out_file.save()
                return 0, 1

        return rows_inserted, rows_failed


    def process(self):
        
        from models import TransferOutRow, Specimen, Location, SpecimenType
        
        rows_inserted = 0
        rows_failed = 0

        for transfer_out_row in TransferOutRow.objects.filter(fileinfo=self.transfer_out_file, state__in=['pending']):

            try:
                with transaction.atomic():
                    try:
                        to_location = Location.objects.get(name=transfer_out_row.to_location)
                    except Location.DoesNotExist:
                        raise Exception("Location does not exist")

                    try:
                        spec_type = SpecimenType.objects.get(spec_type=transfer_out_row.spec_type)
                    except SpecimenType.DoesNotExist:
                        raise Exception("Specimen Type does not exist")

                    try:
                        specimen = Specimen.objects.get(specimen_label=transfer_out_row.specimen_label, spec_type=spec_type)
                    except Specimen.DoesNotExist:
                        raise Exception("Specimen does not exist")
                    

                    specimen.num_containers=transfer_out_row.num_containers
                    specimen.transfer_out_date = self.float_to_date(transfer_out_row.transfer_out_date)
                    specimen.to_location = to_location
                    specimen.spec_type = spec_type
                    specimen.other_ref = transfer_out_row.other_ref

                    if transfer_out_row.volume:
                        specimen.volume = transfer_out_row.volume
                        specimen.initial_claimed_volume = transfer_out_row.volume
                    else:
                        specimen.volume = None
                        specimen.initial_claimed_volume = None

                    specimen.save()

                    transfer_out_row.state = 'processed'
                    transfer_out_row.error_message = ''
                    transfer_out_row.date_processed = timezone.now()
                    transfer_out_row.save()

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                transfer_out_row.state = 'error'
                transfer_out_row.error_message = e.message
                transfer_out_row.save()

                rows_failed += 1
                continue

        return rows_inserted, rows_failed


class AnnihilationFileHandler(FileHandler):

    def __init__(self, annihilation_file):
        super(AnnihilationFileHandler, self).__init__()
        self.annihilation_file = annihilation_file
        self.excel_annihilation_file = ExcelHelper(f=annihilation_file.data_file.url)
        self.annihilation_row = None

        self.registered_columns = ['parent id',
                                   'child id',
                                   'child volume',
                                   'number of aliquot',
                                   'annihilation date',
                                   'reason',
                                   'panel type',
                                   'panel inclusion criteria']

        self.existing_columns = self.excel_annihilation_file.read_header()


    def parse(self):
        from models import AnnihilationRow

        header = self.excel_annihilation_file.read_header()
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.excel_annihilation_file.nrows):
            try:
                if row_num >= 1:
                    row = self.excel_annihilation_file.read_row(row_num)
                    row_dict = dict(zip(header, row))

                    annihilation_row = AnnihilationRow.objects.create(parent_id=row_dict['parent id'],
                                                                      child_id=row_dict['child id'],
                                                                      child_volume=row_dict['child volume'],
                                                                      number_of_aliquot=row_dict['number of aliquot'],
                                                                      annihilation_date=row_dict['annihilation date'],
                                                                      reason=row_dict['reason'],
                                                                      panel_type=row_dict['panel type'],
                                                                      panel_inclusion_criteria=row_dict['panel inclusion criteria'],
                                                                      fileinfo=self.annihilation_file,
                                                                      state='pending')


                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.annihilation_file.message = "row " + str(row_num) + ": " + e.message
                self.annihilation_file.save()
                return 0, 1

        return rows_inserted, rows_failed


    def process(self):
        
        from models import AnnihilationRow, Specimen, Reason, AliquotingReason, PanelInclusionCriteria
        
        rows_inserted = 0
        rows_failed = 0

        for annihilation_row in AnnihilationRow.objects.filter(fileinfo=self.annihilation_file, state__in=['pending']):

            try:
                with transaction.atomic():
                    
                    reason, reason_created = Reason.objects.get_or_create(name=annihilation_row.reason)
                    aliquoting_reason, aliquoting_reason_created = AliquotingReason.objects.get_or_create(name=annihilation_row.panel_type)
                    panel_inclusion_criteria, panel_inclusion_criteria_created = PanelInclusionCriteria.objects.get_or_create(name=annihilation_row.panel_inclusion_criteria)

                    if annihilation_row.parent_id == annihilation_row.child_id:
                        try:
                            parent_specimen = Specimen.objects.get(specimen_label=annihilation_row.parent_id, parent_label=None)
                        except Specimen.DoesNotExist:
                            raise Exception("Specimen does not exist")
                        
                        parent_specimen.num_containers = annihilation_row.number_of_aliquot
                        parent_specimen.volume = annihilation_row.child_volume
                        parent_specimen.modified_date = self.float_to_date(annihilation_row.annihilation_date)
                        parent_specimen.reason = reason
                        parent_specimen.aliquoting_reason = aliquoting_reason
                        parent_specimen.panel_inclusion_criteria = panel_inclusion_criteria
                        parent_specimen.save()

                    else:
                        try:
                            parent_specimen = Specimen.objects.get(specimen_label=annihilation_row.parent_id, parent_label=None)
                        except Specimen.DoesNotExist:
                            raise Exception("Specimen does not exist")

                        parent_specimen.modified_date = self.float_to_date(annihilation_row.annihilation_date)
                        parent_specimen.save()

                        Specimen.objects.update_or_create(specimen_label=annihilation_row.child_id,
                                                          parent_label=annihilation_row.parent_id,
                                                          num_containers=annihilation_row.number_of_aliquot,
                                                          volume=annihilation_row.child_volume,
                                                          spec_type=parent_specimen.spec_type,
                                                          reported_draw_date=parent_specimen.reported_draw_date,
                                                          source_study=parent_specimen.source_study,
                                                          created_date=self.float_to_date(annihilation_row.annihilation_date),
                                                          reason=reason,
                                                          aliquoting_reason=aliquoting_reason,
                                                          panel_inclusion_criteria=panel_inclusion_criteria)

                    annihilation_row.state = 'processed'
                    annihilation_row.error_message = ''
                    annihilation_row.date_processed = timezone.now()
                    annihilation_row.save()

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                annihilation_row.state = 'error'
                annihilation_row.error_message = e.message
                annihilation_row.save()

                rows_failed += 1
                continue

        return rows_inserted, rows_failed


class MissingTransferOutFileHandler(FileHandler):
    missing_transfer_out_file = None

    def __init__(self, missing_transfer_out_file):
        super(MissingTransferOutFileHandler, self).__init__()
        self.missing_transfer_out_file = missing_transfer_out_file
        self.excel_missing_transfer_out_file = ExcelHelper(f=missing_transfer_out_file.data_file.url)
        self.missing_transfer_out_row = None

    def parse(self):
        
        from models import MissingTransferOutRow
        
        rows_inserted = 0
        rows_failed = 0
        sheets = self.excel_missing_transfer_out_file.wb.sheet_names()
        allowed_sheets = ['evaluation panel','development panel 100ul','development panel 500ul']

        for sheet in sheets:

            current_sheet = self.excel_missing_transfer_out_file.wb.sheet_by_name(sheet)
            header = [x.lower() for x in current_sheet.row_values(0)]

            if current_sheet.name.lower() in allowed_sheets:
                for row_num in range(current_sheet.nrows):
                    try:
                        if row_num >= 1:
                            row = current_sheet.row_values(row_num)
                            row_dict = dict(zip(header, row))

                            missing_transfer_out_row = MissingTransferOutRow.objects.create(first_aliquot=row_dict['first aliquot'],
                                                                                            last_aliquot=row_dict['last aliquot'],
                                                                                            aliquots_created=row_dict['aliquots created'],
                                                                                            volume=row_dict['volume'],
                                                                                            panels_used=row_dict['panels used'],
                                                                                            fileinfo=self.missing_transfer_out_file,
                                                                                            state='pending')


                            rows_inserted += 1
                    except Exception, e:
                        logger.exception(e)
                        self.missing_transfer_out_file.message = "row " + str(row_num) + ": " + e.message
                        self.missing_transfer_out_file.save()
                        return 0, 1

        return rows_inserted, rows_failed


    def process(self):
        
        from models import MissingTransferOutRow, Specimen
        
        rows_inserted = 0
        rows_failed = 0

        for missing_transfer_out_row in MissingTransferOutRow.objects.filter(fileinfo=self.missing_transfer_out_file, state__in=['pending']):
            try:
                first_aliquot = missing_transfer_out_row.first_aliquot.split('-')
                last_aliquot = missing_transfer_out_row.last_aliquot.split('-')
                
                if first_aliquot[0] == last_aliquot[0]:
                    with transaction.atomic():
                        for aliquot_number in range(int(first_aliquot[1]), int(last_aliquot[1]) + 1):
                            specimen = Specimen.objects.create(specimen_label=first_aliquot[0] + '-' + str(aliquot_number),
                                                               created_at = timezone.now(),
                                                               volume=missing_transfer_out_row.volume)

                            missing_transfer_out_row.state = 'processed'
                            missing_transfer_out_row.date_processed = timezone.now()
                            missing_transfer_out_row.save()

                            rows_inserted += 1
                else:
                    raise Exception("Aliquot range does not match")

            except Exception, e:
                logger.exception(e)
                missing_transfer_out_row.state = 'error'
                missing_transfer_out_row.error_message = e.message
                missing_transfer_out_row.save()
                
                rows_failed += 1
                continue

        return rows_inserted, rows_failed


#ALL HANDLERS MUST BE REGISTERED HERE
register_file_handler("subject", SubjectFileHandler)
register_file_handler("visit", VisitFileHandler)
register_file_handler("annihilation", AnnihilationFileHandler)
register_file_handler("transfer_out", TransferOutFileHandler)
register_file_handler("transfer_in", TransferInFileHandler)
register_file_handler("missing_transfer_out", MissingTransferOutFileHandler)

