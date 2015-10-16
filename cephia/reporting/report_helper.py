from django.db import connection
from collections import defaultdict, OrderedDict

class Report(object):

    def prepare_report(self, raw_sql, num_rows=None):
        self.raw_sql = raw_sql
        self.num_rows = num_rows or 20
        self._run()

    def _run(self):
        cursor = connection.cursor()
        cursor.execute(self.raw_sql)
        self._headers = [col[0] for col in cursor.description]
        self._rows = [ OrderedDict(zip(self.headers, row)) for row in cursor.fetchall()[0:self.num_rows] ]

    @property
    def headers(self):
        return self._headers

    @property
    def rows(self):
        return self._rows
    