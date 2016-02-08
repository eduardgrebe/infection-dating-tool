from file_handler import FileHandler
from handler_imports import *
import logging

logger = logging.getLogger(__name__)

class ProtocolLookupFileHandler(FileHandler):
    upload_file = None
    
    def __init__(self, upload_file):
        super(ProtocolLookupFileHandler, self).__init__(upload_file)

        self.registered_columns = ['Protocol',
                                   'TestCode',
                                   'TestId']

    def process(self):
        from diagnostics.models import ProtocolLookup, DiagnosticTest
        
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    if not row_dict['TestId'] or 'or' in row_dict['TestId']:
                        continue
                    else:
                        try:
                            protocol_lookup = ProtocolLookup.objects.get(name=row_dict['TestCode'])
                            protocol_lookup.protocol = row_dict['Protocol']
                            protocol_lookup.test = DiagnosticTest.objects.get(pk=row_dict['TestId'])
                            protocol_lookup.save()
                        except ProtocolLookup.DoesNotExist:
                            ProtocolLookup.objects.create(name=row_dict['TestCode'],
                                                          protocol=row_dict['Protocol'],
                                                          test=DiagnosticTest.objects.get(pk=row_dict['TestId']))

                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1

        self.upload_file.state = 'processed'
        self.upload_file.save()
        return rows_inserted, rows_failed
