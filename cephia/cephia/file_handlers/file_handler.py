from datetime import datetime, date
import logging
import xlrd

logger = logging.getLogger(__name__)


class FileHandler(object):

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
