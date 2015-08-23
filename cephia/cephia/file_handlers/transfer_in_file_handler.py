from file_handler import FileHandler


class TransferInFileHandler(FileHandler):
    transfer_in_file = None

    def __init__(self, transfer_in_file):
        super(TransferInFileHandler, self).__init__()
        self.transfer_in_file = transfer_in_file
        self.excel_transfer_in_file = ExcelHelper(f=transfer_in_file.data_file.url)

        self.registered_columns = ['specimen_label',
                                   'subject_label',
                                   'drawdate_year',
                                   'drawdate_month',
                                   'drawdate_day',
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
                                   'notes',
                                   'visit_linkage']


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
                    
                    transfer_in_row = TransferInRow.objects.create(specimen_label=row_dict['specimen label'],
                                                                   subject_label=row_dict['subject_label'],
                                                                   drawdate_year=row_dict['drawdate_year'],
                                                                   drawdate_month=row_dict['drawdate_month'],
                                                                   drawdate_day=row_dict['drawdate_day'])

                    transfer_in_row.number_of_containers = row_dict['number_of_containers']
                    transfer_in_row.transfer_date_yyyy = row_dict['transfer_date_yyyy']
                    transfer_in_row.transfer_date_mm = row_dict['transfer_date_mm']
                    transfer_in_row.transfer_date_dd = row_dict['transfer_date_dd']
                    transfer_in_row.receiving_site = row_dict['receiving_site']
                    transfer_in_row.transfer_reason = row_dict['transfer_reason']
                    transfer_in_row.volume = row_dict['volume']
                    transfer_in_row.volume_units = row_dict['volume_units']
                    transfer_in_row.specimen_type = row_dict['specimen_type']
                    transfer_in_row.source_study = row_dict['source_study'],
                    transfer_in_row.notes = row_dict['notes'],
                    transfer_in_row.visit_linkage = row_dict['visit_linkage']
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

    def validate(self, row):
        from cephia.models import TransferInRow
        
        default_less_date = datetime.now().date() - relativedelta(years=75)
        default_more_date = datetime.now().date() + relativedelta(years=75)
        
        for transfer_in_row in TransferInRow.objects.filter(fileinfo=self.visit_file, state='pending'):
            try:
                self.register_dates()
                if not self.registered_dates['draw_date'] < self.registered_dates['transfer_date']:
                    raise Exception('draw_date must be smaller than transfer_date')

                if not self.registered_dates['aids_diagnosis_date'] > datetime.now().date():
                    raise Exception('ars_onset_date must be smaller than first_positive_date')

                if row_dict['specimen_type'] in ['1','3','4.1','4.2','6', '8']:
                    if row_dict['volume_units'] != 'cards':
                        raise Exception('volume_units must be "cards" for this specimen_type')
                if row_dict['volume'] < 20:
                    raise Exception('volume must be less than 20 for this specimen type')

                if row_dict['specimen_type'] == '2':
                    if row_dict['volume_units'] != 'grams':
                        raise Exception('volume_units must be "grams" for this specimen')
                    if row_dict['volume'] < 100:
                        raise Exception('volume must be less than 100 for this specimen')

                if row_dict['specimen_type'] in ['5.1','5.2']:
                    if row_dict['volume_units'] != 'm cells':
                        raise Exception('volume_units must be "cards" for this specimen_type')
                    if row_dict['volume'] < 20:
                        raise Exception('volume must be less than 20 for this specimen')

                if row_dict['specimen_type'] == '7':
                    if row_dict['volume_units'] != 'swabs':
                        raise Exception('volume_units must be "swabs" for this specimen_type')
                    if row_dict['volume'] < 20:
                        raise Exception('volume must be less than 20 for this specimen')

                if row_dict['specimen_type'] in ['10.1','10.2']:
                    if row_dict['volume'] > 90:
                        raise Exception('volume must be greater than 90 for this specimen type')
                    
                transfer_in_row.state = 'validated'
                transfer_in_row.error_message = ''
                transfer_in_row.save()
            except Exception, e:
                logger.exception(e)
                transfer_in_row.state = 'error'
                transfer_in_row.error_message = e.message
                transfer_in_row.save()
                continue

        #reason, reason_created = Reason.objects.get_or_create(name=transfer_in_row.transfer_reason)
        # try:
        #     SpecimenType.objects.get(spec_type=transfer_in_row.spec_type)
        # except SpecimenType.DoesNotExist:
        #     raise Exception("SpecimenType does not exist")

    def process(self):
        from models import TransferInRow, Subject, Study, Reason, SpecimenType, Specimen, Site
        
        rows_inserted = 0
        rows_failed = 0

        for transfer_in_row in TransferInRow.objects.filter(fileinfo=self.transfer_in_file, state__in=['pending']):

            try:
                with transaction.atomic():
                    try:
                        subject = Subject.objects.get(patient_label=transfer_in_row.patient_label)
                    except Site.DoesNotExist:
                        subject = None
                        pass

                    specimen, specimen_created = Specimen.objects.get_or_create(specimen_label = transfer_in_row.specimen_label,
                                                                                reported_draw_date = self.get_date(transfer_in_row.draw_date),
                                                                                transfer_in_date = self.get_date(transfer_in_row.transfer_in_date),
                                                                                reason = reason,
                                                                                subject = subject,
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
