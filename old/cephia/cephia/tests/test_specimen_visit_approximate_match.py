import logging
from cephia.tests.test_base import TestBase
from cephia.models import *
from django.core.management import call_command

logger = logging.getLogger(__name__)

class TestSpecimenVisitApproximateMatch(TestBase):
    def setUp(self):
        super(TestSpecimenVisitApproximateMatch, self).setUp()

        self.subjects = self.create_fileinfo('subject.xlsx', 'test_case_005')
        self.visits = self.create_fileinfo('visit.xlsx', 'test_case_005')
        self.transfer_ins = self.create_fileinfo('transfer_in.xlsx', 'test_case_005')
        
    def test_approximate_matches(self):
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

        self.assertEqual(Visit.objects.get(visit_date='2014-11-10').pk, Specimen.objects.get(specimen_label='AS10-10544').visit.pk)
        self.assertEqual(Visit.objects.get(visit_date='2014-12-01').pk, Specimen.objects.get(specimen_label='AS11-08365').visit.pk)
        self.assertEqual(Visit.objects.get(visit_date='2014-12-01').pk, Specimen.objects.get(specimen_label='AS11-08366').visit.pk)
        self.assertEqual(Visit.objects.get(visit_date='2014-07-01').pk, Specimen.objects.get(specimen_label='AS11-08367').visit.pk)
