from file_handler import FileHandler
from handler_imports import *
import logging

logger = logging.getLogger(__name__)
class TransferOutFileHandler(FileHandler):
    
    def __init__(self, upload_file):
        super(TransferOutFileHandler, self).__init__(upload_file)
        
        self.registered_columns = ['specimen_label',
                                   'number_of_containers',
                                   'specimen_type',
                                   'volume',
                                   'volume_units',
                                   'shipped_in_panel',
                                   'shipment_date_yyyy',
                                   'shipment_date_mm',
                                   'shipment_date_dd',
                                   'destination_site']

    def parse(self):
        from cephia.models import TransferOutRow
        
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))

                    if row_dict.get('id', None):
                        transfer_out_row = TransferOutRow.objects.get(pk=row_dict['id'])
                    else:
                        transfer_out_row = TransferOutRow.objects.create(specimen_label=row_dict['specimen_label'],
                                                                         fileinfo=self.upload_file)
                    
                    transfer_out_row.number_of_containers=row_dict['number_of_containers']
                    transfer_out_row.specimen_type=row_dict['specimen_type']
                    transfer_out_row.volume=row_dict['volume']
                    transfer_out_row.volume_units=row_dict['volume_units']
                    transfer_out_row.shipped_in_panel=row_dict['shipped_in_panel']
                    transfer_out_row.shipment_date_yyyy=row_dict['shipment_date_yyyy']
                    transfer_out_row.shipment_date_mm=row_dict['shipment_date_mm']
                    transfer_out_row.shipment_date_dd=row_dict['shipment_date_dd']
                    transfer_out_row.destination_site=row_dict['destination_site']
                    transfer_out_row.fileinfo=self.upload_file
                    transfer_out_row.state='pending'
                    transfer_out_row.save()

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1

        return rows_inserted, rows_failed

    def validate(self):
        from cephia.models import TransferOutRow, Specimen, SpecimenType, Site
        
        default_less_date = datetime.now().date() - relativedelta(years=75)
        default_more_date = datetime.now().date() + relativedelta(years=75)
        rows_validated = 0
        rows_failed = 0
        
        for transfer_out_row in TransferOutRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''
                self.register_dates(transfer_out_row.model_to_dict())

                try:
                    Site.objects.get(name=transfer_out_row.destination_site)
                except Site.DoesNotExist:
                    error_msg += "Site does not exist.\n"
                
                try:
                    specimen_type = SpecimenType.objects.get(spec_type=transfer_out_row.specimen_type)
                except SpecimenType.DoesNotExist:
                    error_msg += "SpecimenType does not exist.\n"
                
                try:
                    specimen = Specimen.objects.get(specimen_label=transfer_out_row.specimen_label, specimen_type=specimen_type)
                except Specimen.DoesNotExist:
                    error_msg += "Specimen does not exist.\n"

                if self.registered_dates['shipment_date'] < (specimen.transfer_in_date or default_less_date):
                    error_msg += "Shipment date cannot be before transfer in date.\n"

                if error_msg:
                    raise Exception(error_msg)

                transfer_out_row.state = 'validated'
                transfer_out_row.error_message = ''
                rows_validated += 1
                transfer_out_row.save()
            except Exception, e:
                logger.exception(e)
                transfer_out_row.state = 'error'
                transfer_out_row.error_message = e.message
                rows_failed += 1
                transfer_out_row.save()
                continue

        return rows_validated, rows_failed

    def process(self):
        
        from cephia.models import TransferOutRow, Specimen, SpecimenType, Site
        
        rows_inserted = 0
        rows_failed = 0

        for transfer_out_row in TransferOutRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            try:
                self.register_dates(transfer_out_row.model_to_dict())
                
                with transaction.atomic():
                    specimen = Specimen.objects.get(specimen_label=transfer_out_row.specimen_label,
                                                    specimen_type=SpecimenType.objects.get(spec_type=transfer_out_row.specimen_type))
                    
                    specimen.number_of_containers = transfer_out_row.number_of_containers
                    specimen.transfer_out_date = self.registered_dates.get('shipment_date', None)
                    specimen.modified_date = timezone.now()
                    specimen.receiving_site = Site.objects.get(name=transfer_out_row.destination_site)
                    specimen.save()

                    transfer_out_row.state = 'processed'
                    transfer_out_row.error_message = ''
                    transfer_out_row.date_processed = timezone.now()
                    transfer_out_row.specimen = specimen
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
