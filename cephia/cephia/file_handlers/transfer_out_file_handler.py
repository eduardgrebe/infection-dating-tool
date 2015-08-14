class TransferOutFileHandler(FileHandler):
    transfer_out_file = None
    
    def __init__(self, transfer_out_file):
        super(TransferOutFileHandler, self).__init__()
        self.transfer_out_file = transfer_out_file
        self.excel_transfer_out_file = ExcelHelper(f=transfer_out_file.data_file.url)

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

                    #this is to ignore blanks and can probably be done better
                    if not row_dict['spec_id']:
                        continue

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

    def validate(self, row):
        pass

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
                    specimen.transfer_out_date = self.get_date(transfer_out_row.transfer_out_date)
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
