from django.db import connection
from collections import OrderedDict

class Report(object):

    def prepare_report(self, raw_sql, num_rows=None):
        self.raw_sql = raw_sql
        self.num_rows = num_rows
        self._run()

    def _run(self):
        cursor = connection.cursor()
        cursor.execute(self.raw_sql)
        self._headers = [col[0] for col in cursor.description]
        self._rows = [ OrderedDict(zip(self.headers, row)) for row in cursor.fetchall()]
        if self.num_rows:
            self._rows = self._rows[0:self.num_rows]

    @property
    def headers(self):
        return self._headers

    def add_header(self, header):
        if header not in self._headers:
            self._headers.append(header)

    def remove_header(self, header):
        del self._headers[self._headers.index(header)]
            
    def set_rows(self, new_rows):
        self._rows = new_rows
    
    @property
    def rows(self):
        return self._rows
    
