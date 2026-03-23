from file_handler import FileHandler
from handler_imports import *
import logging

logger = logging.getLogger(__name__)

class PanelMembershipFileHandler(FileHandler):
    upload_file = None
    
    def __init__(self, upload_file):
        super(PanelMembershipFileHandler, self).__init__(upload_file)

        self.registered_columns = ['visit_id',
                                   'category',
                                   'panel_inclusion_criterion',
                                   'n_replicates']


    def parse(self):
        from assay.models import PanelMembershipRow

        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    panel_membership_row = PanelMembershipRow.objects.create(visit=row_dict['visit_id'],
                                                                             category=row_dict['category'],
                                                                             panel_inclusion_criterion=row_dict['panel_inclusion_criterion'],
                                                                             replicates=row_dict['n_replicates'],
                                                                             state='pending',
                                                                             fileinfo=self.upload_file)

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1

        if rows_failed > 0:
            self.upload_file.state = 'row_error'
        else:
            self.upload_file.state = 'imported'
        fail_msg = 'Failed to import ' + str(rows_failed) + ' rows.'
        success_msg = 'Successfully imported ' + str(rows_inserted) + ' rows.'

        self.upload_file.message += fail_msg + '\n' + success_msg + '\n'
        self.upload_file.save()

    def validate(self):
        from cephia.models import Visit
        from assay.models import PanelMembershipRow, PanelMembership, Panel

        rows_validated = 0
        rows_failed = 0

        for membership_row in PanelMembershipRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''

                try:
                    viist = Visit.objects.get(pk=membership_row.visit)
                except Visit.DoesNotExist:
                    error_msg += "Visit not recognised.\n"

                if error_msg:
                    raise Exception(error_msg)

                membership_row.state = 'validated'
                membership_row.error_message = ''
                rows_validated += 1
                membership_row.save()
            except Exception, e:
                logger.exception(e)
                membership_row.state = 'error'
                membership_row.error_message = e.message
                rows_failed += 1
                membership_row.save()
                continue

        if rows_failed > 0:
            self.upload_file.state = 'row_error'
        else:
            self.upload_file.state = 'validated'
        fail_msg = 'Failed to validate ' + str(rows_failed) + ' rows.'
        success_msg = 'Successfully validated ' + str(rows_validated) + ' rows.'

        self.upload_file.message += fail_msg + '\n' + success_msg + '\n'
        self.upload_file.save()

    def process(self, panel_id):
        from cephia.models import Visit, Panel
        from assay.models import PanelMembershipRow, PanelMembership

        rows_inserted = 0
        rows_failed = 0

        for panel_membership_row in PanelMembershipRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            try:
                with transaction.atomic():
                    panel_membership = PanelMembership.objects.create(visit=Visit.objects.get(pk=panel_membership_row.visit),
                                                                      category=panel_membership_row.category,
                                                                      replicates=panel_membership_row.replicates,
                                                                      panel_inclusion_criterion=panel_membership_row.panel_inclusion_criterion,
                                                                      panel=Panel.objects.get(pk=panel_id))

                    panel_membership_row.state = 'processed'
                    panel_membership_row.date_processed = timezone.now()
                    panel_membership_row.error_message = ''
                    panel_membership_row.save()
                    rows_inserted += 1

            except Exception, e:
                logger.exception(e)
                panel_membership_row.state = 'error'
                panel_membership_row.error_message = e.message
                panel_membership_row.save()
                rows_failed += 1
                continue

        if rows_failed > 0:
            self.upload_file.state = 'row_error'
        else:
            self.upload_file.state = 'processed'
        fail_msg = 'Failed to process ' + str(rows_failed) + ' rows.'
        success_msg = 'Successfully processed ' + str(rows_inserted) + ' rows.'
        
        self.upload_file.message += fail_msg + '\n' + success_msg + '\n'
        self.upload_file.save()
