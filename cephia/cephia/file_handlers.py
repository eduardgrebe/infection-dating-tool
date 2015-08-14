from excel_helper import ExcelHelper
from datetime import datetime, date
from django.db import transaction
from django.utils import timezone
import logging
import xlrd

logger = logging.getLogger(__name__)

class FileHandler(object):
    
    registered_file_handlers = []

    def __init__(self):
        register_file_handler("visit", VisitFileHandler)
        register_file_handler("annihilation", AnnihilationFileHandler)
        register_file_handler("transfer_out", TransferOutFileHandler)
        register_file_handler("transfer_in", TransferInFileHandler)
        register_file_handler("missing_transfer_out", MissingTransferOutFileHandler)
        
    def register_file_handler(file_type, cls):
        registered_file_handlers.append( (file_type, cls) )

    def get_file_handler_for_type(file_type):
        for registered_file_type, registered_file_handler in registered_file_handlers:
            if file_type == registered_file_type:
                return registered_file_handler
            raise Exception("Unknown file type: %s" % file_type)
        
    def get_date(self, value):
        if value:
            if ('/' in value) or ('-' in value):
                return datetime.strptime(value, "%Y-%m-%d").date()        
            else:
                return datetime(*xlrd.xldate_as_tuple(float(value), 0)).date()
        else:
            return None

    def get_year(self, year_string):
        if year_string:
            return date(int(year_string), 1, 1)
        else:
            return None

    def get_bool(self, bool_string):
        return bool_string == '1'

    def validate_file(self):
        missing_cols = list(set(self.registered_columns) - set(self.existing_columns))
        extra_cols = list(set(self.existing_columns) - set(self.registered_columns))

        if missing_cols:
            raise Exception("The following columns are missing from your file %s" % str(missing_cols))

        if extra_cols:
            return "Your file contained the following extra columns and they have been ignored %s" % str(extra_cols)
            




