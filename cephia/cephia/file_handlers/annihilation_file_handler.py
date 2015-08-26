from file_handler import FileHandler


class AnnihilationFileHandler(FileHandler):

    def __init__(self, aliquot_file):
        super(AliquotFileHandler, self).__init__()
        self.aliquot_file = aliquot_file
        self.excel_aliquot_file = ExcelHelper(f=aliquot_file.data_file.url)
        self.aliquot_row = None

        self.registered_columns = ['parent_label',
                                   'aliquot_label',
                                   'aliquoting_date_yyyy',
                                   'aliquoting_date_mm',
                                   'aliquoting_date_dd',
                                   'specimen_type',
                                   'volume',
                                   'volume_units',
                                   'reason']

        self.existing_columns = self.excel_aliquot_file.read_header()

    def parse(self):
        from models import AliquotRow

        header = self.excel_aliquot_file.read_header()
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.excel_aliquot_file.nrows):
            try:
                if row_num >= 1:
                    row = self.excel_aliquot_file.read_row(row_num)
                    row_dict = dict(zip(header, row))
                    
                    aliquot_row = AliquotRow.objects.create(parent_label=row_dict['parent_label'],
                                                            aliquot_label=row_dict['aliquot_label'],
                                                            volume=row_dict['volume'],
                                                            volume_units=row_dict['volume_units'],
                                                            aliquoting_date_yyyy=row_dict['aliquoting_date_yyyy'],
                                                            aliquoting_date_mm=row_dict['aliquoting_date_mm'],
                                                            aliquoting_date_dd=row_dict['aliquoting_date_dd'],
                                                            aliquot_reason=row_dict['reason'],
                                                            fileinfo=self.aliquot_file,
                                                            state='pending')


                    rows_inserted += 1

            except Exception, e:
                logger.exception(e)
                self.aliquot_file.message = "row " + str(row_num) + ": " + e.message
                self.aliquot_file.save()
                return 0, 1

        return rows_inserted, rows_failed


    def process(self):
        
        from models import AliquotRow, Specimen
        
        rows_inserted = 0
        rows_failed = 0

        for aliquot_row in AliquotRow.objects.filter(fileinfo=self.aliquot_file, state__in=['pending']):

            try:
                with transaction.atomic():
                    if aliquot_row.parent_id == aliquot_row.child_id:
                        try:
                            parent_specimen = Specimen.objects.get(specimen_label=aliquot_row.parent_id, parent_label=None)
                        except Specimen.DoesNotExist:
                            raise Exception("Specimen does not exist")
                            
                        parent_specimen.num_containers = aliquot_row.number_of_aliquot
                        parent_specimen.volume = aliquot_row.child_volume
                        parent_specimen.modified_date = self.get_date(aliquot_row.aliquot_date)
                        parent_specimen.reason = reason
                        parent_specimen.aliquoting_reason = aliquoting_reason
                        parent_specimen.panel_inclusion_criteria = panel_inclusion_criteria
                        parent_specimen.save()

                    else:
                        try:
                            parent_specimen = Specimen.objects.get(specimen_label=aliquot_row.parent_id, parent_label=None)
                        except Specimen.DoesNotExist:
                            raise Exception("Specimen does not exist")

                        parent_specimen.modified_date = self.get_date(aliquot_row.aliquot_date)
                        parent_specimen.save()

                        Specimen.objects.get_or_create(specimen_label=aliquot_row.child_id,
                                                       parent_label=aliquot_row.parent_id,
                                                       num_containers=aliquot_row.number_of_aliquot,
                                                       volume=aliquot_row.child_volume,
                                                       spec_type=parent_specimen.spec_type,
                                                       reported_draw_date=parent_specimen.reported_draw_date,
                                                       source_study=parent_specimen.source_study,
                                                       created_date=self.get_date(aliquot_row.aliquot_date),
                                                       reason=reason,
                                                       aliquoting_reason=aliquoting_reason)
                    aliquot_row.state = 'processed'
                    aliquot_row.error_message = ''
                    aliquot_row.date_processed = timezone.now()
                    aliquot_row.save()

                    rows_inserted += 1

            except Exception, e:
                logger.exception(e)
                aliquot_row.state = 'error'
                aliquot_row.error_message = e.message
                aliquot_row.save()
                rows_failed += 1
                continue

        return rows_inserted, rows_failed
