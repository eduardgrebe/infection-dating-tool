class AnnihilationFileHandler(FileHandler):

    def __init__(self, annihilation_file):
        super(AnnihilationFileHandler, self).__init__()
        self.annihilation_file = annihilation_file
        self.excel_annihilation_file = ExcelHelper(f=annihilation_file.data_file.url)
        self.annihilation_row = None

        self.registered_columns = ['parent_label',
                                   'aliquot_label',
                                   'aliquoting_date_yyyy',
                                   'aliquoting_date_mm',
                                   'aliquoting_date_dd',
                                   'specimen_type',
                                   'volume',
                                   'volume_units',
                                   'reason']

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

                    #this is to ignore blanks and can probably be done better
                    if not row_dict['parent id']:
                        continue
                    
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
                        parent_specimen.modified_date = self.get_date(annihilation_row.annihilation_date)
                        parent_specimen.reason = reason
                        parent_specimen.aliquoting_reason = aliquoting_reason
                        parent_specimen.panel_inclusion_criteria = panel_inclusion_criteria
                        parent_specimen.save()

                    else:
                        try:
                            parent_specimen = Specimen.objects.get(specimen_label=annihilation_row.parent_id, parent_label=None)
                        except Specimen.DoesNotExist:
                            raise Exception("Specimen does not exist")

                        parent_specimen.modified_date = self.get_date(annihilation_row.annihilation_date)
                        parent_specimen.save()

                        Specimen.objects.get_or_create(specimen_label=annihilation_row.child_id,
                                                       parent_label=annihilation_row.parent_id,
                                                       num_containers=annihilation_row.number_of_aliquot,
                                                       volume=annihilation_row.child_volume,
                                                       spec_type=parent_specimen.spec_type,
                                                       reported_draw_date=parent_specimen.reported_draw_date,
                                                       source_study=parent_specimen.source_study,
                                                       created_date=self.get_date(annihilation_row.annihilation_date),
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
