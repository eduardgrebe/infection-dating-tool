from file_handler import FileHandler
from handler_imports import *
import logging

logger = logging.getLogger(__name__)

class DiagnosticTestFileHandler(FileHandler):
    upload_file = None
    
    def __init__(self, upload_file):
        super(DiagnosticTestFileHandler, self).__init__(upload_file)

        self.registered_columns = ['id',
                                   'name',
                                   'description']

    def process(self):
        from diagnostics.models import DiagnosticTest
        
        rows_inserted = 0
        rows_failed = 0

        for row_num in range(self.num_rows):
            try:
                if row_num >= 1:
                    row_dict = dict(zip(self.header, self.file_rows[row_num]))
                    DiagnosticTest.objects.update_or_create(id=row_dict['id'],
                                                            name=row_dict['name'],
                                                            description=row_dict['description'])
                    
                    rows_inserted += 1
            except Exception, e:
                logger.exception(e)
                self.upload_file.message = "row " + str(row_num) + ": " + e.message
                self.upload_file.save()
                return 0, 1
            
        self.upload_file.state = 'processed'
        self.upload_file.save()
