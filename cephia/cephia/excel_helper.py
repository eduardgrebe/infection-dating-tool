# -*- coding: utf-8 -*-

import xlrd, xlwt
import cStringIO
import datetime
import time

import logging
logger = logging.getLogger(__name__)

TICK='R'
NOTICK='£'

class ExcelHelper(object):
    def __init__(self, f=None, sheet_number=0, sheet_name=None, write=False):
        """ different arguments are required depending on the value of 'write' """
        super(ExcelHelper, self).__init__()

        self.wb = None

        if write:
            self._open_for_write(sheet_name)
        else:
            self._open_for_read(f, sheet_number)

    def add_sheet(self, name, sheet_number):
        self.sheet = self.wb.add_sheet(name)
        self.sheet_number  = sheet_number
        self.x = 0
        self.y = 0

    def _open_for_read(self, f, sheet_number):
        self.sheet_number = sheet_number
        self.wb = xlrd.open_workbook(f)
        self._goto_sheet(int(sheet_number))

    def _open_for_write(self, sheet_name):
        self.wb = xlwt.Workbook(encoding='utf-8')
        self.sheet = self.wb.add_sheet(sheet_name) 
        self.sheet_number = 0
        self.x = 0
        self.y = 0
        self.tick_style = xlwt.easyxf('font: name Wingdings 2')
        self.date_style = xlwt.XFStyle()
        self.date_style.num_format_str = 'M/D/YY h:mm'
        self.bold_style = xlwt.easyxf('font: bold on; align: horiz center')
        self.bold_left_style = xlwt.easyxf('font: bold on; align: horiz left')
        self.center_style = xlwt.easyxf('align: horiz center')

    def _goto_sheet(self, index=0):
        try:
            self.sheet_number = index-1
            self.sheet = self.wb.sheets()[self.sheet_number]
        except IndexError:
            raise Exception("No sheet at position %d" % index)
        
    @classmethod
    def _excel_unicode(self, val):
        if type(val) == float:
            if int(val) == val:
                return unicode(int(val))
        return unicode(val)

    def write_row(self, row, style=None):
        for y,d in enumerate(row):
            self.write(d, 0, y, style)
        self.x += 1

    def write(self, value, x_offset=0, y_offset=0, style=None):
        x = self.x + x_offset
        y = self.y + y_offset

        if style:
            self.sheet.write(x, y, value, style)
        elif type(value) == bool:
            value=TICK if d else NOTICK
            self.sheet.write(x, y, value, self.tick_style)
        elif type(value) == datetime.datetime:
            self.sheet.write(x, y, value, self.date_style)
        elif type(value) == datetime.date:
            self.sheet.write(x, y, time.strftime('%Y-%m-%d', value.timetuple()))
        else:
            self.sheet.write(x, y, value)

    def read(self):
        return self._excel_unicode(self.sheet.cell_value(self.x, self.y)).strip()

    def save(self):
        f = cStringIO.StringIO()
        self.wb.save(f)
        f.seek(0)
        return f

    def read_row(self, row, date_cols=[]):
        return [ self._excel_unicode(self.as_date(self.sheet.cell_value(row, col))).strip() if col in date_cols else self._excel_unicode(self.sheet.cell_value(row,col)).strip() for col in range(self.sheet.ncols) ]

    def read_header(self):
        return [ v.lower() for v in self.read_row(0) ]

    def read_double_line_header(self):
        headings_0_raw = self.read_row(0)
        prev = ''
        headings_0 = []
        for x in headings_0_raw:
            if len(x.strip())>0:
                prev = x
            headings_0.append(prev)
        headings_1 = self.read_row(1)
        headings = [ "%s:%s"%(x.lower(),y.lower()) for x,y in zip(headings_0, headings_1) ]
        return headings

    def map_header_to_original(self):
        double_line_header = self.read_header()
        original = self.read_row(0)
        return dict( zip(double_line_header, original) )
        
    def set_cols_width(self, widths):
        for i,w in enumerate(widths):
            self.sheet.col(i).width = w

    @property
    def stats(self):
        return { 'sheet_name': [self.sheet.name, 'Sheet name'] }

    @property
    def nrows(self):
        return self.sheet.nrows

    @property
    def ncols(self):
        return self.sheet.ncols

    @classmethod
    def as_bool(self, value):
        return value==TICK or value=='R' or value.upper()=='X' # 'R' is the checkbox wingding, X is just the letter X

    def as_date(self, value):
        if value:
            return datetime.datetime(*xlrd.xldate_as_tuple(value, self.wb.datemode))
        else:
            return ''
    
    
