import logging
from cephia.tests.test_base import TestBase
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
        self.create_ethnicities()
        self.create_countries()
        self.create_source_study()
        self.create_specimen_type()
        
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
