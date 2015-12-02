import logging
from cephia.test_helper.test_base import TestBase
from cephia.models import *
from django.core.management import call_command

logger = logging.getLogger(__name__)

class TestCase001(TestBase):
    def setUp(self):
        super(TestCase001, self).setUp()
        
        self.subjects = self.create_fileinfo('subject.xlsx', 'test_case_001')
        self.visits = self.create_fileinfo('visit.xlsx', 'test_case_001')
        self.transfer_ins = self.create_fileinfo('transfer_in.xlsx', 'test_case_001')
        self.aliquots = self.create_fileinfo('aliquot.xlsx', 'test_case_001')
        self.transfer_outs = self.create_fileinfo('transfer_out.xlsx', 'test_case_001')

        
    def test_case_001(self):
        self.subjects.get_handler().parse()
        self.assertEqual(1, SubjectRow.objects.filter(fileinfo=self.subjects, state='pending').count())

        self.subjects.get_handler().validate()
        self.assertEqual(1, SubjectRow.objects.filter(fileinfo=self.subjects, state='validated').count())

        self.subjects.get_handler().process()
        self.assertEqual(1, SubjectRow.objects.filter(fileinfo=self.subjects, state='processed').count())
        self.assertEqual(1, Subject.objects.all().count())

        self.visits.get_handler().parse()
        self.assertEqual(2, VisitRow.objects.filter(fileinfo=self.visits, state='pending').count())

        self.visits.get_handler().validate()
        self.assertEqual(2, VisitRow.objects.filter(fileinfo=self.visits, state='validated').count())

        self.visits.get_handler().process()
        self.assertEqual(2, VisitRow.objects.filter(fileinfo=self.visits, state='processed').count())
        self.assertEqual(2, Visit.objects.all().count())

        call_command('associate_subject_visit')
        self.assertEqual(Visit.objects.all().count(), Visit.objects.filter(subject__isnull=False).count())
        
        self.transfer_ins.get_handler().parse()
        self.assertEqual(2, TransferInRow.objects.filter(fileinfo=self.transfer_ins, state='pending').count())

        self.transfer_ins.get_handler().validate()
        self.assertEqual(2, TransferInRow.objects.filter(fileinfo=self.transfer_ins, state='validated').count())

        self.transfer_ins.get_handler().process()
        self.assertEqual(2, TransferInRow.objects.filter(fileinfo=self.transfer_ins, state='processed').count())
        self.assertEqual(2, Specimen.objects.all().count())

        call_command('associate_specimen_subject')
        self.assertEqual(Specimen.objects.all().count(), Specimen.objects.filter(subject__isnull=False).count())
        
        call_command('associate_specimen_visit')
        self.assertEqual(Specimen.objects.all().count(), Specimen.objects.filter(visit__isnull=False).count())

        self.aliquots.get_handler().parse()
        self.assertEqual(7, AliquotRow.objects.filter(fileinfo=self.aliquots, state='pending').count())

        self.aliquots.get_handler().validate()
        self.assertEqual(7, AliquotRow.objects.filter(fileinfo=self.aliquots, state='validated').count())

        self.aliquots.get_handler().process()
        self.assertEqual(7, AliquotRow.objects.filter(fileinfo=self.aliquots, state='processed').count())
        self.assertEqual(7, Specimen.objects.all().count())

        call_command('parent_child_inheritance')
        self.assertEqual(Specimen.objects.all().count(), Specimen.objects.filter(visit__isnull=False).count())
        
        self.transfer_outs.get_handler().parse()
        self.assertEqual(5, TransferOutRow.objects.filter(fileinfo=self.transfer_outs, state='pending').count())

        self.transfer_outs.get_handler().validate()
        self.assertEqual(5, TransferOutRow.objects.filter(fileinfo=self.transfer_outs, state='validated').count())

        self.transfer_outs.get_handler().process()
        self.assertEqual(5, TransferOutRow.objects.filter(fileinfo=self.transfer_outs, state='processed').count())
        self.assertEqual(7, Specimen.objects.all().count())

        self.assertEqual(5, Specimen.objects.filter(shipped_to__isnull=False).count())

        self.assertEqual(6, Specimen.objects.filter(is_available=False).count())


class TestCase002(TestBase):
    def setUp(self):
        super(TestCase002, self).setUp()

        self.subjects = self.create_fileinfo('subject.docx', 'test_case_002')

    def test_case_002(self):
        try:
            handler = self.subjects.get_handler()
        except Exception, e:
            self.assertEqual("Invalid file type. Only .csv and .xls/x are supported.", e.message)


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

class TestTransferinVolumeArithmetic(TestBase):
    def setUp(self):
        super(TestTransferinVolumeArithmetic, self).setUp()

        self.transfer_ins = self.create_fileinfo('transfer_in.xlsx', 'test_case_006')

    def test_volume_rollup(self):
        self.transfer_ins.get_handler().parse()
        self.transfer_ins.get_handler().validate()
        self.transfer_ins.get_handler().process()
        
        self.assertEqual(1, Specimen.objects.filter(specimen_label='AS10-10544').count())
        self.assertEqual(4, Specimen.objects.get(specimen_label='AS10-10544').number_of_containers)
        self.assertEqual(10000, Specimen.objects.get(specimen_label='AS10-10544').initial_claimed_volume)

    def test_multicontainer_volume(self):
        self.transfer_ins.get_handler().parse()
        self.transfer_ins.get_handler().validate()
        self.transfer_ins.get_handler().process()

        self.assertEqual(1, Specimen.objects.filter(specimen_label='AS10-10545').count())
        self.assertEqual(4, Specimen.objects.get(specimen_label='AS10-10545').number_of_containers)
        self.assertEqual(4000, Specimen.objects.get(specimen_label='AS10-10545').initial_claimed_volume)

    def test_rollup_and_multicontainer_volume(self):
        self.transfer_ins.get_handler().parse()
        self.transfer_ins.get_handler().validate()
        self.transfer_ins.get_handler().process()

        self.assertEqual(1, Specimen.objects.filter(specimen_label='AS10-10546').count())
        self.assertEqual(5, Specimen.objects.get(specimen_label='AS10-10546').number_of_containers)
        self.assertEqual(4600, Specimen.objects.get(specimen_label='AS10-10546').initial_claimed_volume)




