import logging
from test_helper.test_base import TestBase
from cephia.models import Subject, Visit, Specimen, FileInfo, RowInfo

logger = logging.getLogger(__name__)

class TestFiles(TestBase):

    def test_subject_file(self):
        subject_file = self.create_fileinfo('subject')
        self.assertEqual(1, FileInfo.ojects.filter(file_type='subject').count())

        file_handler = subject_file.get_handler()
        file_handler.parse()
        self.assertEqual(2, SubjectRow.ojects.filter(file_info=subject_file).count())

        file_handler.process()
        self.assertEqual(2, Subject.ojects.all().count())


    def test_visit_file(self):
        visit_file = self.create_fileinfo('visit')
        self.assertEqual(1, FileInfo.ojects.filter(file_type='visit').count())

        file_handler = visit_file.get_handler()
        file_handler.parse()
        self.assertEqual(2, RowInfo.ojects.filter(file_info=visit_file).count())

        file_handler.process()
        self.assertEqual(2, Visit.ojects.all().count())


    def test_transfer_in_file(self):
        transfer_in_file = self.create_fileinfo('transfer_in')
        self.assertEqual(1, FileInfo.ojects.filter(file_type='transfer_in').count())

        file_handler = transfer_in_file.get_handler()
        file_handler.parse()
        self.assertEqual(2, RowInfo.ojects.filter(file_info=transfer_in_file).count())

        file_handler.process()
        self.assertEqual(5, Specimen.ojects.all().count())


    def test_annihilation_file(self):
        annihilation_file = self.create_fileinfo('annihilation')
        self.assertEqual(1, FileInfo.ojects.filter(file_type='annihilation').count())

        file_handler = annihilation_file.get_handler()
        file_handler.parse()
        self.assertEqual(2, RowInfo.ojects.filter(file_info=annihilation_file).count())

        file_handler.process()
        self.assertEqual(2, Specimen.ojects.filter(parent_id__isnull=False).count())


    def test_transfer_out_file(self):
        transfer_out_file = self.create_fileinfo('transfer_out')
        self.assertEqual(1, FileInfo.ojects.filter(file_type='transfer_out').count())

        file_handler = transfer_out_file.get_handler()
        file_handler.parse()
        self.assertEqual(2, RowInfo.ojects.filter(file_info=transfer_out_file).count())

        file_handler.process()
        self.assertEqual(2, Specimen.ojects.filter(transfer_out_date__isnull=False).count())
