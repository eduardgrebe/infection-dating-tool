import logging
from cephia.test_helper.test_base import TestBase
from cephia.models import *
from django.core.management import call_command

logger = logging.getLogger(__name__)

class TestSpecimenVisitExactMatch(TestBase):
    def setUp(self):
        super(TestSpecimenVisitExactMatch, self).setUp()

        self.subjects = self.create_fileinfo('subject.xlsx', 'test_case_004')
        self.visits = self.create_fileinfo('visit.xlsx', 'test_case_004')
        self.transfer_ins = self.create_fileinfo('transfer_in.xlsx', 'test_case_004')

    def test_exact_matches(self):
        self.subjects.get_handler().parse()
        self.subjects.get_handler().validate()
        self.subjects.get_handler().process()
        self.visits.get_handler().parse()
        self.visits.get_handler().validate()
        self.visits.get_handler().process()
        self.transfer_ins.get_handler().parse()
        self.transfer_ins.get_handler().validate()
        self.transfer_ins.get_handler().process()

        call_command('associate_subject_visit')
        call_command('associate_specimen_subject')
        call_command('associate_specimen_visit')

        self.assertEqual(2, Specimen.objects.filter(subject__isnull=False).count())
        self.assertEqual(1, Specimen.objects.filter(visit__isnull=False).count())
        self.assertEqual(1, Specimen.objects.filter(specimen_label='AS10-10544', visit__isnull=False).count())
        self.assertEqual(1, Specimen.objects.filter(specimen_label='AS11-08365', visit__isnull=True).count())
