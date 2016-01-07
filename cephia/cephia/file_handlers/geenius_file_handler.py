from file_handler import FileHandler
from handler_imports import *
import logging

logger = logging.getLogger(__name__)

class GeeniusFileHandler(FileHandler):
    upload_file = None
    
    def __init__(self, upload_file):
        super(GeeniusFileHandler, self).__init__(upload_file)

        self.registered_columns = ['Blinded ID',
                                   'Assay',
                                   'Sample Type',
                                   'SITE',
                                   'Test Date',
                                   'Operator',
                                   'Assay Kit Lot',
                                   'Run/Plate ID',
                                   'Test Mode',
                                   'Well',
                                   'gp36',
                                   'gp140',
                                   'gp160',
                                   'gp24',
                                   'gp41',
                                   'CTRL',
                                   'Geenius Confirmatory Result',
                                   'Panel Type',
                                   'Exclude']


    def parse(self):
        from assay.models import GeeniusResultRow
        
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    self.header = [ x.strip() for x in self.header ]
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    
                    geenius_result_row = GeeniusResultRow.objects.create(blinded_id=row_dict['Blinded ID'],
                                                                         assay=row_dict['Assay'],
                                                                         samples=row_dict['Samples'],
                                                                         site=row_dict['SITE'],
                                                                         test_date=row_dict['Test Date'],
                                                                         operator=row_dict['Operator'],
                                                                         assay_kit_lot_id=row_dict['Assay Kit Lot:'],
                                                                         plate_id=row_dict['Run/Plate IDs'],
                                                                         test_mode=row_dict['Test Mode'],
                                                                         well=row_dict['Wells'],
                                                                         gp36=row_dict['gp36'],
                                                                         gp140=row_dict['gp140'],
                                                                         gp160=row_dict['gp160'],
                                                                         gp41=row_dict['gp41'],
                                                                         p24=row_dict['p24'],
                                                                         p31=row_dict['p31'],
                                                                         ctrl=row_dict['CTRL'],
                                                                         biorad_confirmatory_result=row_dict['BioRad Confirmatory Result'],
                                                                         panel_type=row_dict['Panel Type'],
                                                                         exclude=row_dict['Exclude'],
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
        from assay.models import GeeniusResultRow
        
        rows_validated = 0
        rows_failed = 0
        
        for geenius_result_row in GeeniusResultRow.objects.filter(fileinfo=self.upload_file, state='pending'):
            try:
                error_msg = ''
                
                # try:
                #     Specimen.objects.get(pk=geenius_result_row.specimen)
                # except Specimen.DoesNotExist:
                #     error_msg += "Specimen not recognised.\n"

                # try:
                #     Panel.objects.get(pk=geenius_result_row.panel)
                # except Panel.DoesNotExist:
                #     error_msg += "Panel not recognised.\n"

                if error_msg:
                    raise Exception(error_msg)
                
                geenius_result_row.state = 'validated'
                geenius_result_row.error_message = ''
                rows_validated += 1
                geenius_result_row.save()
            except Exception, e:
                logger.exception(e)
                geenius_result_row.state = 'error'
                geenius_result_row.error_message = e.message
                rows_failed += 1
                geenius_result_row.save()
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
        from assay.models import GeeniusResultRow, GeeniusResult
        
        rows_inserted = 0
        rows_failed = 0

        for geenius_result_row in GeeniusResultRow.objects.filter(fileinfo=self.upload_file, state='validated'):
            try:
                with transaction.atomic():
                    geenius_result = GeeniusResult.objects.create(specimen=Specimen.objects.get(pk=geenius_result_row.specimen),
                                                                assay=Assay.objects.get(pk=geenius_result_row.assay),
                                                                sample_type=geenius_result_row.sample_type,
                                                                site=Site.objects.get(name=geenius_result_row.site),
                                                                test_date=self.registered_dates(),
                                                                operator=geenius_result_row.operator,
                                                                assay_kit_lot_id=geenius_result_row.assay_kit_lot_id,
                                                                plate_id=geenius_result_row.plate_id,
                                                                test_mode=geenius_result_row.test_mode,
                                                                well=geenius_result_row.well,
                                                                intermediate_1=geenius_result_row.intermediate_1,
                                                                intermediate_2=geenius_result_row.intermediate_2,
                                                                intermediate_3=geenius_result_row.intermediate_3,
                                                                intermediate_4=geenius_result_row.intermediate_4,
                                                                intermediate_5=geenius_result_row.intermediate_5,
                                                                intermediate_6=geenius_result_row.intermediate_6,
                                                                final_result=geenius_result_row.final_result,
                                                                panel_type=geenius_result_row.panel_type)
                    
                    geenius_result_row.state = 'processed'
                    geenius_result_row.date_processed = timezone.now()
                    geenius_result_row.error_message = ''
                    geenius_result_row.save()
                    rows_inserted += 1

            except Exception, e:
                logger.exception(e)
                geenius_result_row.state = 'error'
                geenius_result_row.error_message = e.message
                geenius_result_row.save()
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
