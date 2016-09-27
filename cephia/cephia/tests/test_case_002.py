import logging
from cephia.test_helper.test_base import TestBase
from cephia.models import *
from django.core.management import call_command

logger = logging.getLogger(__name__)

class TestCase002(TestBase):
    def setUp(self):
        super(TestCase002, self).setUp()

        self.subjects = self.create_fileinfo('subject.docx', 'test_case_002')

    def test_case_002(self):
        try:
            handler = self.subjects.get_handler()
        except Exception, e:
            self.assertEqual("Invalid file type. Only .csv and .xls/x are supported.", e.message)
