from django.test import TestCase
import logging
from cephi.models import FileInfo

logger = logging.getLogger(__name__)

class TestHelper(object):
    """ Put helper functions that all tests can use in this class """

    def __init__(self, *args, **kwargs):
        super(TestHelper, self).__init__(*args, **kwargs)

    def create_fileinfo(self, filename, file_type):
        return FileInfo.objects.create(filename=filename,
                                       file_type=file_type,
                                       state='pending')


class TestBase(TestCase, TestHelper):
    """ All tests should extend from this class """
    pass

