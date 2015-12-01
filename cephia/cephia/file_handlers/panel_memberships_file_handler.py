from file_handler import FileHandler
from handler_imports import *
import logging

logger = logging.getLogger(__name__)

class PanelMembershipsFileHandler(FileHandler):
    upload_file = None
    
    def __init__(self, upload_file):
        super(PanelMembershipsFileHandler, self).__init__(upload_file)

        self.registered_columns = ['visit',
                                   'panel',
                                   'replicates']

    def parse(self):
        from assay.models import PanelMembershipRow
        
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    
                    panel_membership_row = PanelMembershipRow.objects.create(visit=row_dict['visit'],
                                                                             panel=row_dict['panel'],
                                                                             replicates=row_dict['replicates'],
                                                                             state='pending',
                                                                             fileinfo=self.upload_file)

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1

        return rows_inserted, rows_failed

    def validate(self):
        from cephia.models import Visit
        from assay.models import PanelMembershipRow, PanelMembership, Panel
        
        rows_validated = 0
        rows_failed = 0
        
        for visit_row in VisitRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                if :
                    error_msg += 'scope_visit_ec must be null if source study is not "SCOPE".\n'
        
                if error_msg:
                    raise Exception(error_msg)
                
                visit_row.state = 'validated'
                visit_row.error_message = ''
                rows_validated += 1
                visit_row.save()
            except Exception, e:
                logger.exception(e)
                visit_row.state = 'error'
                visit_row.error_message = e.message
                rows_failed += 1
                visit_row.save()
                continue

        return rows_validated, rows_failed
        

    def process(self):
        from assay.models import PanelMembership, PanelMembershipRow
        
        rows_inserted = 0
        rows_failed = 0

        for panel_membership_row in PanelMembershipRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            try:
                with transaction.atomic():
                    panel_membership = PanelMembership.objects.create(visit=Visit.objects.get(pk=panel_membership_row.visit)
                                                                      panel=Panel.objects.get(pk=panel_membership_row.panel),
                                                                      replicates=panel_membership_row.replicates)

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
                    
        return rows_inserted, rows_failed
