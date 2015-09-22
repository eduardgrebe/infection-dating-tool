from file_handler import FileHandler
from handler_imports import *
import logging
import os

logger = logging.getLogger(__name__)


class TransferInFileHandler(FileHandler):
    upload_file = None

    def __init__(self, upload_file):
        super(TransferInFileHandler, self).__init__(upload_file)

        self.registered_columns = ['specimen_label',
                                   'subject_label',
                                   'drawdate_yyyy',
                                   'drawdate_mm',
                                   'drawdate_dd',
                                   'number_of_containers',
                                   'transfer_date_yyyy',
                                   'transfer_date_mm',
                                   'transfer_date_dd',
                                   'receiving_site',
                                   'transfer_reason',
                                   'specimen_type',
                                   'volume',
                                   'volume_units',
                                   'source_study',
                                   'notes']


    def parse(self):
        from cephia.models import TransferInRow
        
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))

                    if row_dict.get('id', None):
                        transfer_in_row = TransferInRow.objects.get(pk=row_dict['id'])
                    else:
                        transfer_in_row = TransferInRow.objects.create(specimen_label=row_dict['specimen_label'],
                                                                       subject_label=row_dict['subject_label'],
                                                                       drawdate_yyyy=row_dict['drawdate_yyyy'],
                                                                       drawdate_mm=row_dict['drawdate_mm'],
                                                                       drawdate_dd=row_dict['drawdate_dd'],
                                                                       fileinfo=self.upload_file)

                    transfer_in_row.number_of_containers = row_dict['number_of_containers']
                    transfer_in_row.transfer_date_yyyy = row_dict['transfer_date_yyyy']
                    transfer_in_row.transfer_date_mm = row_dict['transfer_date_mm']
                    transfer_in_row.transfer_date_dd = row_dict['transfer_date_dd']
                    transfer_in_row.receiving_site = row_dict['receiving_site']
                    transfer_in_row.transfer_reason = row_dict['transfer_reason']
                    transfer_in_row.volume = row_dict['volume']
                    transfer_in_row.volume_units = row_dict['volume_units']
                    transfer_in_row.specimen_type = row_dict['specimen_type']
                    transfer_in_row.source_study = row_dict['source_study']
                    transfer_in_row.notes = row_dict['notes']
                    transfer_in_row.state = 'pending'
                    transfer_in_row.error_message = ''
                    transfer_in_row.fileinfo=self.upload_file
                    transfer_in_row.save()

                    rows_inserted += 1

            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1

        return rows_inserted, rows_failed

    def validate(self):
        from cephia.models import TransferInRow, SpecimenType, Specimen
        
        default_less_date = datetime.now().date() - relativedelta(years=75)
        default_more_date = datetime.now().date() + relativedelta(years=75)
        rows_validated = 0
        rows_failed = 0
        
        for transfer_in_row in TransferInRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''
                self.register_dates(transfer_in_row.model_to_dict())

                row_exists = TransferInRow.objects.filter(specimen_label=transfer_in_row.specimen_label,
                                                          specimen_type=transfer_in_row.specimen_type,
                                                          fileinfo=self.upload_file).exists()
                if row_exists:
                    transfer_in_row.roll_up = True
                    transfer_in_row.save()

                exists = Specimen.objects.filter(specimen_label=transfer_in_row.specimen_label,
                                                 specimen_type__spec_type=transfer_in_row.specimen_type).exists()
                if exists:
                    error_msg += 'This specimen already exists.\n'

                if not transfer_in_row.volume:
                    error_msg += 'Volume is required.\n'

                if not transfer_in_row.volume_units:
                    error_msg += 'Volume units is required.\n'
                
                if not transfer_in_row.number_of_containers:
                    error_msg += 'Number of containers is required.\n'
                
                if not self.registered_dates.get('drawdate', default_less_date) < self.registered_dates.get('transfer_date', default_more_date):
                    error_msg += 'draw_date must be before transfer_date. '

                if not self.registered_dates.get('transfer_date', default_less_date) <= datetime.now().date():
                    error_msg += 'transfer_date before today.\n'

                try:
                    SpecimenType.objects.get(spec_type=transfer_in_row.specimen_type)
                except SpecimenType.DoesNotExist:
                    error_msg += "SpecimenType does not exist.\n"

                if not transfer_in_row.subject_label:
                    error_msg += "Specimen must have a claimed subject.\n"

                if transfer_in_row.specimen_type in ['1','3','4.1','4.2','6', '8']:
                    if transfer_in_row.volume_units != 'microlitres':
                        error_msg += 'volume_units must be "microlitres" for this specimen_type.\n'
                    if float(transfer_in_row.volume or 0) < 90:
                        error_msg += 'volume must be greater than 90 for this specimen type.\n'

                if transfer_in_row.specimen_type == '2':
                    if transfer_in_row.volume_units not in ['cards','microlitres']:
                        error_msg += 'volume_units must be either "cards" or "microlitres" for this specimen.\n'
                    if transfer_in_row.volume_units == 'cards' and float(transfer_in_row.volume or 0) > 20:
                        error_msg += 'volume must be less than 20 for this specimen.\n'
                    if transfer_in_row.volume_units == 'microlitres' and float(transfer_in_row.volume or 0) < 20:
                        error_msg += 'volume must be greater than 20 for this specimen.\n'

                if transfer_in_row.specimen_type in ['5.1','5.2']:
                    if transfer_in_row.volume_units != 'grams':
                        error_msg += 'volume_units must be "grams" for this specimen_type.\n'
                    if float(transfer_in_row.volume or 0) > 100:
                        error_msg += 'volume must be less than 100 for this specimen.\n'

                if transfer_in_row.specimen_type == '7':
                    if transfer_in_row.volume_units not in ['m cells', 'microlitres']:
                        error_msg += 'volume_units must be either "m cells" or "microlitres" for this specimen_type.\n'
                    if transfer_in_row.volume_units == 'm cells' and float(transfer_in_row.volume or 0) > 20:
                        error_msg += 'volume must be less than 20 for this specimen.\n'
                    if transfer_in_row.volume_units == 'microlitres' and float(transfer_in_row.volume or 0) < 90:
                        error_msg += 'volume must be greater than 90 for this specimen.\n'

                if transfer_in_row.specimen_type in ['10.1','10.2']:
                    if transfer_in_row.volume_units != 'swabs':
                        error_msg += 'volume_units must be "swabs" for this specimen_type.\n'
                    if float(transfer_in_row.volume or 0) > 10:
                        error_msg += 'volume must be less than or equal to 10 for this specimen type.\n'

                if error_msg:
                    raise Exception(error_msg) 


                transfer_in_row.state = 'validated'
                transfer_in_row.error_message = ''
                rows_validated += 1
                transfer_in_row.save()
            except Exception, e:
                logger.exception(e)
                transfer_in_row.state = 'row_error'
                transfer_in_row.error_message = e.message
                rows_failed += 1
                transfer_in_row.save()
                continue

        return rows_validated, rows_failed

    def process(self):
        from cephia.models import TransferInRow, Subject, Study, SpecimenType, Specimen, Site
        
        rows_inserted = 0
        rows_failed = 0
        validated_records = TransferInRow.objects.filter(fileinfo=self.upload_file, state='validated')#, roll_up=False)
        # validated_records_roll_up = TransferInRow.objects.filter(fileinfo=self.upload_file,
        #                                                          state='validated', roll_up=True).annotate(containers=Sum('volume'),
        #                                                                                                    volume=Sum('volume'))
        
        for transfer_in_row in validated_records:
            try:
                self.register_dates(transfer_in_row.model_to_dict())
                
                with transaction.atomic():
                    try:
                        if transfer_in_row.subject_label == 'Unknown':
                            subject = Subject.objects.create(subject_label='artificial_' + transfer_in_row.specimen_label)
                            subject.aritificial = True
                            subject.save()
                        else:
                            subject = Subject.objects.get(subject_label=transfer_in_row.subject_label)
                    except Subject.DoesNotExist:
                        subject = None
                        pass

                    specimen = Specimen.objects.create(specimen_label = transfer_in_row.specimen_label,
                                                       subject_label = transfer_in_row.subject_label,
                                                       reported_draw_date = self.registered_dates.get('drawdate', None),
                                                       transfer_in_date = self.registered_dates.get('transfer_date', None),
                                                       transfer_reason = transfer_in_row.transfer_reason,
                                                       subject = subject,
                                                       specimen_type = SpecimenType.objects.get(spec_type=transfer_in_row.specimen_type),
                                                       number_of_containers = (transfer_in_row.number_of_containers or None),
                                                       initial_claimed_volume = (transfer_in_row.volume or None),
                                                       volume_units = transfer_in_row.volume_units,
                                                       source_study = None,
                                                       receiving_site = Site.objects.get(name=transfer_in_row.receiving_site))

                    transfer_in_row.state = 'processed'
                    transfer_in_row.date_processed = timezone.now()
                    transfer_in_row.specimen = specimen
                    transfer_in_row.save()
                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                transfer_in_row.state = 'row_error'
                transfer_in_row.error_message = e.message
                transfer_in_row.save()

                rows_failed += 1
                continue
        # import pdb; pdb.set_trace()
        # for transfer_in_row in validated_records_roll_up:
        #     try:
        #         self.register_dates(transfer_in_row.model_to_dict())
                
        #         with transaction.atomic():
        #             try:
        #                 if transfer_in_row.subject_label == 'Unknown':
        #                     subject = Subject.objects.create(subject_label='artificial_' + transfer_in_row.specimen_label)
        #                     subject.aritificial = True
        #                     subject.save()
        #                 else:
        #                     subject = Subject.objects.get(subject_label=transfer_in_row.subject_label)
        #             except Subject.DoesNotExist:
        #                 subject = None
        #                 pass

        #             specimen = Specimen.objects.create(specimen_label = transfer_in_row.specimen_label,
        #                                                subject_label = transfer_in_row.subject_label,
        #                                                reported_draw_date = self.registered_dates.get('drawdate', None),
        #                                                transfer_in_date = self.registered_dates.get('transfer_date', None),
        #                                                transfer_reason = transfer_in_row.transfer_reason,
        #                                                subject = subject,
        #                                                specimen_type = SpecimenType.objects.get(spec_type=transfer_in_row.specimen_type),
        #                                                number_of_containers = (transfer_in_row.number_of_containers or None),
        #                                                initial_claimed_volume = (transfer_in_row.volume or None),
        #                                                volume_units = transfer_in_row.volume_units,
        #                                                source_study = None,
        #                                                receiving_site = Site.objects.get(name=transfer_in_row.receiving_site))

        #             transfer_in_row.state = 'processed'
        #             transfer_in_row.date_processed = timezone.now()
        #             transfer_in_row.specimen = specimen
        #             transfer_in_row.save()
        #             rows_inserted += 1
        #     except Exception, e:
        #         logger.exception(e)
        #         transfer_in_row.state = 'row_error'
        #         transfer_in_row.error_message = e.message
        #         transfer_in_row.save()

        #         rows_failed += 1
        #         continue
        return rows_inserted, rows_failed
