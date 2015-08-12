from django.test import TestCase
import logging
from cephi.models import FileInfo

logger = logging.getLogger(__name__)

class TestHelper(object):
    """ Put helper functions that all tests can use in this class """

    def __init__(self, *args, **kwargs):
        super(TestHelper, self).__init__(*args, **kwargs)

    def get_file(self, file_type):
        import pdb; pdb.set_trace()
        return open(settings.TEST_FILE_ROOT + file_type)
    
    def create_fileinfo(self, file_type):
        excel_file = self.get_file(file_type)
        return FileInfo.objects.create(data_file=excel_file,
                                       file_type=file_type,
                                       state='pending')


class TestBase(TestCase, TestHelper):
    """ All tests should extend from this class """
    pass

