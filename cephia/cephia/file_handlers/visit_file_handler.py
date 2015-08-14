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

                    #this is to ignore blanks and can probably be done better
                    if not row_dict['visit_pt_id']:
                        continue
                    
                    visit_row = VisitRow.objects.create(patient_label=row_dict['visit_pt_id'],
                                                        visit_date=row_dict['visit_date'],
                                                        fileinfo=self.visit_file)

                    visit_row.patient_label = row_dict['visit_pt_id']
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
                    exists = Visit.objects.filter(patient_label=visit_row.patient_label, visit_date=self.get_date(visit_row.visit_date)).exists()
                    if exists:
                        raise Exception("Visit already exists")

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

                    Visit.objects.create(visit_date = self.get_date(visit_row.visit_date),
                                         status = visit_row.status,
                                         study = study,
                                         visit_cd4 = cd4,
                                         visit_vl = vl,
                                         scope_visit_ec = visit_row.scope_visit_ec,
                                         visit_pregnant = self.get_bool(visit_row.visit_pregnant),
                                         visit_hepatitis = self.get_bool(visit_row.visit_hepatitis),
                                         patient_label = visit_row.patient_label)

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
