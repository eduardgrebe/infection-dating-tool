from file_handler import FileHandler
from handler_imports import *
import logging

logger = logging.getLogger(__name__)
from django.core.management import call_command


class ViralLoadFileHandler(FileHandler):

    def __init__(self, upload_file):
        super(ViralLoadFileHandler, self).__init__(upload_file)

        self.registered_columns = ['specimen_label',
                                   'relation',
                                   'value',
                                   'comment',
                                   ]

    def parse(self):
        from cephia.models import ViralLoadRow

        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    
                    if row_dict.get('id', None):
                        viral_load_row = ViralLoadRow.objects.get(
                            pk=row_dict['id'],
                            state__in=['error', 'pending', 'validated', 'imported']
                        )
                        viral_load_row.state = 'pending-fix'
                    else:
                        viral_load_row = ViralLoadRow.objects.create(
                            specimen_label=row_dict['specimen_label'],
                            relation=row_dict['relation'],
                            comment=row_dict['comment'],
                            value=row_dict['value'],
                            fileinfo=self.upload_file
                        )
                        viral_load_row.state='pending'
                        
                    viral_load_row.error_message = ''
                    viral_load_row.fileinfo=self.upload_file
                    viral_load_row.save()

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1

        return rows_inserted, rows_failed
    
    def validate(self):
        from cephia.models import ViralLoadRow, Specimen, SpecimenType
        
        default_less_date = datetime.now().date() - relativedelta(years=75)
        default_more_date = datetime.now().date() + relativedelta(years=75)
        rows_validated = 0
        rows_failed = 0
        
        for viral_load_row in ViralLoadRow.objects.filter(fileinfo=self.upload_file, state__in=['pending', 'pending-fix']):
            try:
                specimen = Specimen.objects.get(specimen_label=viral_load_row.specimen_label)
                float(viral_load_row.value)
                if viral_load_row.relation not in ['', '<', '>']:
                    raise Exception(u"Invalid relation: %s" % viral_load_row.relation)
                if viral_load_row.state != 'pending-fix' and specimen.visit.vl_cephia is not None:
                    raise Exception("Cephia viral load already imported, currently %s" % specimen.visit.vl_cephia)
                
                viral_load_row.state = 'validated'
                viral_load_row.error_message = ''
                rows_validated += 1
                viral_load_row.save()
            except Specimen.DoesNotExist, e:
                viral_load_row.state = 'error'
                viral_load_row.error_message = u"Specimen %s not found" % viral_load_row.specimen_label
                rows_failed += 1
                viral_load_row.save()
                continue
            except Exception, e:
                logger.exception(e)
                viral_load_row.state = 'error'
                viral_load_row.error_message = e.message
                rows_failed += 1
                viral_load_row.save()
                continue

        return rows_validated, rows_failed

    def process(self):
        from cephia.models import ViralLoadRow, Specimen
        
        rows_inserted = 0
        rows_failed = 0

        for viral_load_row in ViralLoadRow.objects.filter(fileinfo=self.upload_file, state='validated'):

            try:
                with transaction.atomic():
                    specimen = Specimen.objects.get(specimen_label=viral_load_row.specimen_label)
                    visit = specimen.visit
                    relation = viral_load_row.relation
                    if not relation:
                        relation = '='
                    visit.vl_cephia = u'%s%s' % (relation, viral_load_row.value)
                    visit.save()

                    viral_load_row.visit = visit
                    viral_load_row.state = 'processed'
                    viral_load_row.error_message = ''
                    viral_load_row.date_processed = timezone.now()
                    viral_load_row.specimen = specimen
                    viral_load_row.save()

                    rows_inserted += 1

            except Exception, e:
                logger.exception(e)
                viral_load_row.state = 'error'
                viral_load_row.error_message = e.message
                viral_load_row.save()
                rows_failed += 1
                continue
        call_command('vl_calculation')
        return rows_inserted, rows_failed
