from datetime import datetime, date
import logging
import xlrd

logger = logging.getLogger(__name__)


class FileHandler(object):

    def register_dates(self, row):
        self.registered_dates = {}
        for key in row:
            is_year = key.split('_')[-1] == 'yyyy'
            if is_year:
                if row[key]:
                    key_list = key.split('_')
                    key_list.remove('yyyy')
                    prefix = '_'.join(key_list)
                    if row[prefix + '_yyyy']:
                        self.registered_dates[prefix] = date(year=int(row[prefix + '_yyyy']),
                                                             month=int(row[prefix + '_mm'] or 1),
                                                             day=int(row[prefix + '_dd'] or 1))
                    else:
                        self.registered_dates[prefix] = None

    def get_date(self, year, month, day):
        input_date = datetime.date(year=year, month=month, day=day)
        min_date = datetime.date(year=1900, month=1, day=1)
        max_date = datetime.now()
        if input_date < min_date:
            raise Exception("Dates cannot be before 1900")
        if input_date > max_date:
            raise Exception("Dates cannot be in the future")

        return input_date

    def get_bool(self, value):
        if value in ['0', 'N']:
            return False
        elif value in ['1', 'Y']:
            return True
        else:
            return None

    def validate_file(self):
        missing_cols = list(set(self.registered_columns) - set(self.existing_columns))
        extra_cols = list(set(self.existing_columns) - set(self.registered_columns))

        if missing_cols:
            raise Exception("The following columns are missing from your file %s" % str(missing_cols))

        if extra_cols:
            return "Your file contained the following extra columns and they have been ignored %s" % str(extra_cols)
