from datetime import datetime, date
import logging
import xlrd
import csv

logger = logging.getLogger(__name__)


class FileHandler(object):

    def __init__(self, upload_file):
        self.upload_file = upload_file
        extension = self.upload_file.get_extension()

        if extension in ['csv','CSV']:
            self.file_rows = self.open_csv(upload_file.data_file.url)
        else:
            raise Exception("Invalid file type. Only .csv and .xls/x are supported.")
            
        self.header = self.file_rows[0]
        self.num_rows = len(self.file_rows)

        self.registered_columns = []

    def excel_unicode(self, val):
        if type(val) == float:
            if int(val) == val:
                return unicode(int(val))
        return unicode(val)

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
        if value.upper() in ['0', 'N', 'FALSE']:
            return False
        elif value.upper() in ['1', 'Y', 'TRUE']:
            return True
        else:
            return None

    def validate_file(self):
        missing_cols = list(set(self.registered_columns) - set(self.header))
        extra_cols = list(set(self.header) - set(self.registered_columns))

        if missing_cols:
            raise Exception("The following columns are missing from your file %s" % str(missing_cols))

        if extra_cols:
            return "Your file contained the following extra columns and they have been ignored %s" % str(extra_cols)


    def open_csv(self, to_read):
        def unicode_csv_reader(unicode_csv_data, dialect = csv.excel, **kwargs):
            csv_reader = csv.reader(unicode_csv_data,
                                    dialect = dialect, **kwargs)
            for row in csv_reader:
                yield [unicode(cell.strip(), 'utf-8') for cell in row]

        try:
            with open(to_read, 'rU') as got_a_file:
                return [line for line in unicode_csv_reader(got_a_file)]
        except (IOError, csv.Error):
            print "Couldn't read from file %s. Exiting." % (to_read)
            raise

    def open_excel(self, to_read):
        def read_lines(workbook):
            sheet = workbook.sheet_by_index(0)
            for row in range(sheet.nrows):
                yield [self.excel_unicode(sheet.cell(row, col).value) for col in range(sheet.ncols)]

        try:
            workbook = xlrd.open_workbook(to_read)
            return [line for line in read_lines(workbook)]
        except (IOError, ValueError):
            print "Couldn't read from file %s. Exiting" % (to_read)
            raise

    def dictfetchall(self, cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
