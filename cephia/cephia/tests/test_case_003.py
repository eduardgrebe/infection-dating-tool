import logging
from cephia.test_helper.test_base import TestBase
from cephia.models import *
from django.core.management import call_command

logger = logging.getLogger(__name__)

class TestCase003(TestBase):
    def setUp(self):
        super(TestCase003, self).setUp()

        self.subjects = self.create_fileinfo('subject.xlsx', 'test_case_003')
        self.visits = self.create_fileinfo('visit.xlsx', 'test_case_003')

    def test_case_003(self):
        self.subjects.get_handler().parse()
        self.subjects.get_handler().validate()
        self.subjects.get_handler().process()
        self.visits.get_handler().parse()
        self.visits.get_handler().validate()
        self.visits.get_handler().process()

        call_command('associate_subject_visit')

        self.assertEqual(1, Visit.objects.filter(subject__isnull=False).count())
        self.assertEqual(1, Visit.objects.filter(subject__isnull=True).count())
