from file_handler import FileHandler

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
        from models import TransferOutRow
        
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))

                    transfer_out_row = TransferOutRow.objects.create(specimen_label=row_dict['spec_id']
                                                                     number_of_containers=row_dict['spec_id']
                                                                     specimen_type=row_dict['spec_id']
                                                                     volume=row_dict['spec_id']
                                                                     volume_units=row_dict['spec_id']
                                                                     shipped_in_panel=row_dict['spec_id']
                                                                     shipment_date_yyyy=row_dict['spec_id']
                                                                     shipment_date_mm=row_dict['spec_id']
                                                                     shipment_date_dd=row_dict['spec_id']
                                                                     destination_site=row_dict['spec_id']
                                                                     fileinfo=self.upload_file,
                                                                     state='pending')


                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1

        return rows_inserted, rows_failed

    def validate(self, row):
        pass

    def process(self):
        
        from models import TransferOutRow, Specimen, Location, SpecimenType
        
        rows_inserted = 0
        rows_failed = 0

        for transfer_out_row in TransferOutRow.objects.filter(fileinfo=self.upload_file, state__in=['pending']):

            try:
                with transaction.atomic():
                    try:
                        spec_type = SpecimenType.objects.get(spec_type=transfer_out_row.specimen_type)
                    except SpecimenType.DoesNotExist:
                        raise Exception("Specimen Type does not exist")

                    try:
                        specimen = Specimen.objects.get(specimen_label=transfer_out_row.specimen_label, spec_type=spec_type)
                    except Specimen.DoesNotExist:
                        raise Exception("Specimen does not exist")
                        

                    specimen.num_containers=transfer_out_row.num_containers
                    specimen.transfer_out_date = self.get_date(transfer_out_row.transfer_out_date)
                    specimen.to_location = to_location
                    specimen.spec_type = spec_type
                    specimen.initial_claimed_volume = transfer_out_row.volume
                    specimen.save()

                    number_of_containers = models.IntegerField(null=True, blank=True)
                    transfer_out_date = models.DateField(null=True, blank=True)
                    modified_date = models.DateField(null=True, blank=True)
                    transfer_reason = models.CharField(max_length=50, null=True, blank=True)
                    subject = models.ForeignKey(Subject, null=True, blank=True)
                    visit = models.ForeignKey(Visit, null=True, blank=True)
                    specimen_type = models.ForeignKey(SpecimenType, null=True, blank=True)
                    volume_units = models.CharField(max_length=20, null=True, blank=True)
                    initial_claimed_volume = models.FloatField(null=True, blank=True)
                    receiving_site = models.ForeignKey(Site, null=True, blank=True)

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
