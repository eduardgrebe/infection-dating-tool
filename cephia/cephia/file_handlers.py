from excel_helper import ExcelHelper
from datetime import datetime
from django.db import transaction
from django.utils import timezone
import logging

registered_file_handlers = []
def register_file_handler(file_type, cls):
    registered_file_handlers.append( (file_type, cls) )

def get_file_handler_for_type(file_type):
    for registered_file_type, registered_file_handler in registered_file_handlers:
        if file_type == registered_file_type:
            return registered_file_handler
    raise Exception("Unknown file type: %s" % file_type)



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
    
    def __init__(self, subject_file, *args, **kwargs):
        super(SubjectFileHandler, self).__init__()
        self.subject_file = subject_file
        self.excel_subject_file = ExcelHelper(f=subject_file.data_file.url)

    def parse(self):

        from models import SubjectRow
        
        header = self.excel_subject_file.read_header()
        date_cols = [1,4,5,6,8,16,17,18,19]
        rows_inserted = 0
        rows_failed = 0
        
        for row_num in range(self.excel_subject_file.nrows):
            try:
                if row_num >= 1:
                    row = self.excel_subject_file.read_row(row_num, date_cols)
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

                    rows_inserted = rows_inserted + 1
            except Exception, e:
                self.subject_file.message = e.message
                self.subject_file.save()
                return 0, 1

        return rows_inserted, rows_failed


    def process(self):

        from models import Ethnicity, Subtype, Country, Subject, SubjectRow
        
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

                    subject = Subject.objects.update_or_create(patient_label=subject_row.patient_label,
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
                    subject_row.date_processed = timezone.now()
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
        super(VisitFileHandler, self).__init__()
        self.visit_file = visit_file
        self.excel_visit_file = ExcelHelper(f=visit_file.data_file.url)

    def parse(self):

        from models import VisitRow
        
        header = self.excel_visit_file.read_header()
        date_cols = [1]
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.excel_visit_file.nrows):
            try:
                if row_num >= 1:
                    row = self.excel_visit_file.read_row(row_num, date_cols)
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

                    rows_inserted = rows_inserted + 1
            except Exception, e:
                self.visit_file.message = e.message
                self.visit_file.save()
                return 0, 1

        return rows_inserted, rows_failed


    def process(self):
        
        from models import VisitRow, Visit, Source
        
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

                    visit = Visit.objects.update_or_create(visit_date = self.get_date(visit_row.visit_date),
                                                           status = visit_row.status,
                                                           source = source,
                                                           visit_cd4 = cd4,
                                                           visit_vl = visit_row.visit_vl,
                                                           scope_visit_ec = visit_row.scope_visit_ec,
                                                           visit_pregnant = self.get_bool(visit_row.visit_pregnant),
                                                           visit_hepatitis = self.get_bool(visit_row.visit_hepatitis),
                                                           visit_label = visit_row.visit_label)

                    visit_row.state = 'processed'
                    visit_row.date_processed = timezone.now()
                    visit_row.error_message = ''
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
        super(TransferInFileHandler, self).__init__()
        self.transfer_in_file = transfer_in_file
        self.excel_transfer_in_file = ExcelHelper(f=transfer_in_file.data_file.url)

    def parse(self):
        
        from models import TransferInRow
        
        header = self.excel_transfer_in_file.read_header()
        date_cols = [2,4]
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.excel_transfer_in_file.nrows):
            try:
                if row_num >= 1:
                    row = self.excel_transfer_in_file.read_row(row_num, date_cols)
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

                    rows_inserted = rows_inserted + 1
            except Exception, e:
                continue
                # self.transfer_in_file.message = e.message
                # self.transfer_in_file.save()
                # return 0, 1

        return rows_inserted, rows_failed


    def process(self):
        
        from models import TransferInRow, Subject, Study, Reason, SpecimenType, Specimen
        
        rows_inserted = 0
        rows_failed = 0

        for transfer_in_row in TransferInRow.objects.filter(fileinfo=self.transfer_in_file, state__in=['pending', 'error']):

            try:
                with transaction.atomic():
                    try:
                        subject = Subject.objects.get(patient_label=transfer_in_row.patient_label)
                    except Subject.DoesNotExist:
                        subject = Subject.objects.create(patient_label=transfer_in_row.patient_label,
                                                         entry_date = timezone.now())
                    
                    study, study_created = Study.objects.get_or_create(name=transfer_in_row.sites)
                    reason, reason_created = Reason.objects.get_or_create(name=transfer_in_row.transfer_reason)
                    spec_type = SpecimenType.objects.get(spec_type=transfer_in_row.spec_type)

                    specimen, specimen_created = Specimen.objects.update_or_create(specimen_label = transfer_in_row.specimen_label,
                                                                                   subject = subject,
                                                                                   reported_draw_date = self.get_date(transfer_in_row.draw_date),
                                                                                   transfer_in_date = self.get_date(transfer_in_row.transfer_in_date),
                                                                                   source_study = study,
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

                    rows_inserted = rows_inserted + 1
            except Exception, e:
                transfer_in_row.state = 'error'
                transfer_in_row.error_message = e.message
                transfer_in_row.save()

                rows_failed = rows_failed + 1
                continue

        return rows_inserted, rows_failed


class TransferOutFileHandler(FileHandler):
    transfer_out_file = None
    
    def __init__(self, transfer_out_file):
        super(TransferOutFileHandler, self).__init__()
        self.transfer_out_file = transfer_out_file
        self.excel_transfer_out_file = ExcelHelper(f=transfer_out_file.data_file.url)

    def parse(self):
        
        from models import TransferOutRow
        
        header = self.excel_transfer_out_file.read_header()
        date_cols = [2]
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.excel_transfer_out_file.nrows):
            try:
                if row_num >= 1:
                    row = self.excel_transfer_out_file.read_row(row_num, date_cols)
                    row_dict = dict(zip(header, row))

                    transfer_out_row = TransferOutRow.objects.create(specimen_label=row_dict['spec_id'],
                                                                     fileinfo=self.transfer_out_file,
                                                                     num_containers=row_dict['#_ containers'],
                                                                     transfer_out_date=row_dict['transfer date'],
                                                                     to_location=row_dict['to location'],
                                                                     transfer_reason=row_dict['reason'],
                                                                     spec_type=row_dict['spec type'],
                                                                     volume=row_dict['vol'],
                                                                     other_ref=row_dict['other id'],
                                                                     state='pending')


                    rows_inserted = rows_inserted + 1
            except Exception, e:
                self.transfer_out_file.message = e.message
                self.transfer_out_file.save()
                return 0, 1

        return rows_inserted, rows_failed


    def process(self):
        
        from models import TransferOutRow, Specimen, Location, SpecimenType
        
        rows_inserted = 0
        rows_failed = 0

        for transfer_out_row in TransferOutRow.objects.filter(fileinfo=self.transfer_out_file, state__in=['pending', 'error']):

            try:
                with transaction.atomic():
                    to_location, location_created = Location.objects.get_or_create(name=transfer_out_row.to_location)
                    spec_type = SpecimenType.objects.get(spec_type=transfer_out_row.spec_type)

                    specimen = Specimen.objects.create(parent_label=transfer_out_row.specimen_label,
                                                       num_containers=transfer_out_row.num_containers,
                                                       transfer_out_date = self.get_date(transfer_out_row.transfer_out_date),
                                                       to_location = to_location,
                                                       spec_type = spec_type,
                                                       other_ref = transfer_out_row.other_ref)

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

                    rows_inserted = rows_inserted + 1
            except Exception, e:
                transfer_out_row.state = 'error'
                transfer_out_row.error_message = e.message
                transfer_out_row.save()

                rows_failed = rows_failed + 1
                continue

        return rows_inserted, rows_failed


class AnnihilationFileHandler(FileHandler):

    def __init__(self, annihilation_file):
        super(AnnihilationFileHandler, self).__init__()
        self.annihilation_file = annihilation_file
        self.excel_annihilation_file = ExcelHelper(f=annihilation_file.data_file.url)
        self.annihilation_row = None

    def parse(self):
        
        from models import AnnihilationRow

        header = self.excel_annihilation_file.read_header()
        date_cols = [4]
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.excel_annihilation_file.nrows):
            try:
                if row_num >= 1:
                    row = self.excel_annihilation_file.read_row(row_num, date_cols)
                    row_dict = dict(zip(header, row))

                    annihilation_row = AnnihilationRow.objects.create(parent_id=row_dict['parent id'],
                                                                      fileinfo=self.annihilation_file,
                                                                      child_id=row_dict['child id'],
                                                                      child_volume=row_dict['child volume'],
                                                                      number_of_aliquot=row_dict['number of aliquot'],
                                                                      annihilation_date=row_dict['annihilation date'],
                                                                      reason=row_dict['reason'],
                                                                      panel_type=row_dict['panel type'],
                                                                      panel_inclusion_criteria=row_dict['panel inclusion criteria'],
                                                                      state='pending')


                    rows_inserted = rows_inserted + 1
            except Exception, e:
                rows_failed = rows_failed + 1
                continue
                # self.annihilation_file.message = e.message
                # self.annihilation_file.save()
                # return 0, 1

        return rows_inserted, rows_failed


    def process(self):
        
        from models import AnnihilationRow, Specimen, Reason, AliquotingReason, PanelInclusionCriteria
        
        rows_inserted = 0
        rows_failed = 0

        for annihilation_row in AnnihilationRow.objects.filter(fileinfo=self.annihilation_file, state__in=['pending', 'error']):

            try:
                with transaction.atomic():

                    reason, reason_created = Reason.objects.get_or_create(name=annihilation_row.reason)
                    aliquoting_reason, aliquoting_reason_created = AliquotingReason.objects.get_or_create(name=annihilation_row.panel_type)
                    panel_inclusion_criteria, panel_inclusion_criteria_created = PanelInclusionCriteria.objects.get_or_create(name=annihilation_row.panel_inclusion_criteria)

                    if annihilation_row.parent_id == annihilation_row.child_id:
                        parent_specimen = Specimen.objects.filter(parent_label=annihilation_row.parent_id, child_label=None)[0] #GETTING THE FIRST IS A HACK
                        
                        parent_specimen.num_containers = annihilation_row.number_of_aliquot
                        parent_specimen.volume = annihilation_row.child_volume
                        parent_specimen.modified_date = self.get_date(annihilation_row.annihilation_date)
                        parent_specimen.reason = reason
                        parent_specimen.aliquoting_reason = aliquoting_reason
                        parent_specimen.panel_inclusion_criteria = panel_inclusion_criteria
                        parent_specimen.save()

                    else:
                        parent_specimen = Specimen.objects.filter(parent_label=annihilation_row.parent_id, child_label=None)[0] #GETTING THE FIRST IS A HACK
                        parent_specimen.modified_date = self.get_date(annihilation_row.annihilation_date)

                        child_specimen = Specimen.objects.create(child_label=annihilation_row.child_id,
                                                                 parent_label=annihilation_row.parent_id,
                                                                 num_containers=annihilation_row.number_of_aliquot,
                                                                 volume=annihilation_row.child_volume,
                                                                 created_date=self.get_date(annihilation_row.annihilation_date),
                                                                 reason=reason,
                                                                 aliquoting_reason=aliquoting_reason,
                                                                 panel_inclusion_criteria=panel_inclusion_criteria)

                    annihilation_row.state = 'processed'
                    annihilation_row.error_message = ''
                    annihilation_row.date_processed = timezone.now()
                    annihilation_row.save()

                    rows_inserted = rows_inserted + 1
            except Exception, e:
                annihilation_row.state = 'error'
                annihilation_row.error_message = e.message
                annihilation_row.save()

                rows_failed = rows_failed + 1
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

        for sheet in sheets:

            current_sheet = self.excel_missing_transfer_out_file.wb.sheet_by_name(sheet)
            header = current_sheet.row(0)
            import pdb; pdb.set_trace()
            for row_num in range(current_sheet.nrows):
                try:
                    if row_num >= 1:
                        row = current_sheet.row(row_num)
                        row_dict = dict(zip(header, row))

                        missing_transfer_out_row = MissingTransferOutRow.objects.create(first_aliquot=row_dict['first aliquot'],
                                                                                        fileinfo=self.missing_transfer_out_file,
                                                                                        last_aliquot=row_dict['last aliquot'],
                                                                                        aliquots_created=row_dict['aliquots created'],
                                                                                        volume=row_dict['volume'],
                                                                                        panels_used=row_dict['panels used'],
                                                                                        state='pending')


                        rows_inserted = rows_inserted + 1
                except Exception, e:
                    rows_failed = rows_failed + 1
                    continue
                # self.missing_transfer_out_file.message = e.message
                # self.missing_transfer_out_file.save()
                # return 0, 1

        return rows_inserted, rows_failed


    def process(self):
        
        from models import MissingTransferOutRow, Specimen
        
        rows_inserted = 0
        rows_failed = 0

        for missing_transfer_out_row in MissingTransferOutRow.objects.filter(fileinfo=self.missing_transfer_out_file, state__in=['pending', 'error']):

            try:
                with transaction.atomic():

                        parent_specimen = Specimen.objects.get(parent_label=missing_transfer_out_row.parent_id, child_label=None)

                        child_specimen = Specimen.objects.create(child_label=missing_transfer_out_row.child_id,
                                                                 parent_label=missing_transfer_out_row.parent_id,
                                                                 num_containers=missing_transfer_out_row.number_of_aliquot,
                                                                 volume=missing_transfer_out_row.child_volume,
                                                                 created_date=missing_transfer_out_row.annihilation_date,
                                                                 reason=reason,
                                                                 aliquoting_reason=aliquoting_reason,
                                                                 panel_inclusion_criteria=panel_inclusion_criteria)

                        missing_transfer_out_row.state = 'processed'
                        missing_transfer_out_row.date_processed = timezone.now()
                        missing_transfer_out_row.save()

                        rows_inserted = rows_inserted + 1
            except Exception, e:
                missing_transfer_out_row.state = 'error'
                missing_transfer_out_row.error_message = e.message
                missing_transfer_out_row.save()
                
                rows_failed = rows_failed + 1
                continue

        return rows_inserted, rows_failed

register_file_handler("visit", VisitFileHandler)
register_file_handler("annihilation", AnnihilationFileHandler)
register_file_handler("transfer_out", TransferOutFileHandler)
register_file_handler("transfer_in", TransferInFileHandler)
register_file_handler("missing_transfer_out", MissingTransferOutFileHandler)
