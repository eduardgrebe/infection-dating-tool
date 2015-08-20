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
                prefix = '_'.join(key.split('_').remove('yyyy'))
                self.registered_dates[prefix] = datetime.date(year=row[prefix + '_yyyy'], month=row[prefix + '_mm'], day=row[prefix + '_dd'])

    def get_date(self, year, month, day):
        input_date = datetime.date(year=year, month=month, day=day)
        min_date = datetime.date(year=1900, month=1, day=1)
        max_date = datetime.now()
        if input_date < min_date:
            raise Exception("Dates cannot be before 1900")
        if input_date > max_date:
            raise Exception("Dates cannot be in the future")

        return input_date

    def validate_file(self):
        missing_cols = list(set(self.registered_columns) - set(self.existing_columns))
        extra_cols = list(set(self.existing_columns) - set(self.registered_columns))

        if missing_cols:
            raise Exception("The following columns are missing from your file %s" % str(missing_cols))

        if extra_cols:
            return "Your file contained the following extra columns and they have been ignored %s" % str(extra_cols)
