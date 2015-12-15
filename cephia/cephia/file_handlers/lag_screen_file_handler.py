from file_handler import FileHandler
from handler_imports import *
import logging

logger = logging.getLogger(__name__)

class LagscreenFileHandler(FileHandler):
    upload_file = None
    
    def __init__(self, upload_file):
        super(LagscreenFileHandler, self).__init__(upload_file)

        self.registered_columns = ['Specimen ID',
                                   'Assay',
                                   'Sample Type',
                                   'Site',
                                   'Test Date',
                                   'Operator',
                                   'Assay Kit Lot ID',
                                   'Run/Plate ID',
                                   'Test Mode',
                                   'Well',
                                   'Intermediate 1',
                                   'Intermediate 2',
                                   'Intermediate 3',
                                   'Intermediate 4',
                                   'Intermediate 5',
                                   'Intermediate 6',
                                   'Final Result',
                                   'Panel Type']


    def parse(self):
        from assay.models import LagscreenRow
        
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    
                    lag_row = LagRow.objects.create(specimen=row_dict['Specimen ID'],
                                                    assay=row_dict['Assay'],
                                                    sample_type=row_dict['Sample Type'],
                                                    site=row_dict['Site'],
                                                    test_date=row_dict['Test Date'],
                                                    operator=row_dict['Operator'],
                                                    assay_kit_lot_id=row_dict['Assay Kit Lot ID'],
                                                    plate_id=row_dict['Run/Plate ID'],
                                                    test_mode=row_dict['Test Mode'],
                                                    well=row_dict['Well'],
                                                    intermediate_1=row_dict['Intermediate 1'],
                                                    intermediate_2=row_dict['Intermediate 2'],
                                                    intermediate_3=row_dict['Intermediate 3'],
                                                    intermediate_4=row_dict['Intermediate 4'],
                                                    intermediate_5=row_dict['Intermediate 5'],
                                                    intermediate_6=row_dict['Intermediate 6'],
                                                    final_result=row_dict['Final Result'],
                                                    panel_type=row_dict['Panel Type'],
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
        from cephia.models import Specimen
        from assay.models import LagscreenRow, Lagscreen, Panel
        
        rows_validated = 0
        rows_failed = 0
        
        for shipment_row in LagscreenRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''
                
                # try:
                #     Specimen.objects.get(pk=shipment_row.specimen)
                # except Specimen.DoesNotExist:
                #     error_msg += "Specimen not recognised.\n"

                # try:
                #     Panel.objects.get(pk=shipment_row.panel)
                # except Panel.DoesNotExist:
                #     error_msg += "Panel not recognised.\n"

                if error_msg:
                    raise Exception(error_msg)
                
                shipment_row.state = 'validated'
                shipment_row.error_message = ''
                rows_validated += 1
                shipment_row.save()
            except Exception, e:
                logger.exception(e)
                shipment_row.state = 'error'
                shipment_row.error_message = e.message
                rows_failed += 1
                shipment_row.save()
                continue
        
        if rows_failed > 0:
            self.upload_file.state = 'row_error'
        else:
            self.upload_file.state = 'validated'
        fail_msg = 'Failed to validate ' + str(rows_failed) + ' rows.'
        success_msg = 'Successfully validated ' + str(rows_validated) + ' rows.'
        
        self.upload_file.message += fail_msg + '\n' + success_msg + '\n'
        self.upload_file.save()

    def process(self):
        from cephia.models import Specimen
        from assay.models import LagscreenRow, Lagscreen, Panel
        
        rows_inserted = 0
        rows_failed = 0

        for panel_shipment_row in LagscreenRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            try:
                with transaction.atomic():
                    panel_shipment = Lagscreen.objects.create(specimen=Specimen.objects.get(pk=panel_shipment_row.specimen),
                                                                  panel=Panel.objects.get(pk=panel_shipment_row.panel),
                                                                  replicates=panel_shipment_row.replicates)

                    panel_shipment_row.state = 'processed'
                    panel_shipment_row.date_processed = timezone.now()
                    panel_shipment_row.error_message = ''
                    panel_shipment_row.save()
                    rows_inserted += 1

            except Exception, e:
                logger.exception(e)
                panel_shipment_row.state = 'error'
                panel_shipment_row.error_message = e.message
                panel_shipment_row.save()
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
