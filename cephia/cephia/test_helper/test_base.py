from django.test import TestCase
import logging
from cephia.models import *
from cephia.file_handlers.file_handler_register import *
from django.core.files import File

logger = logging.getLogger(__name__)

class TestHelper(object):
    """ Put helper functions that all tests can use in this class """

    def __init__(self, *args, **kwargs):
        super(TestHelper, self).__init__(*args, **kwargs)

    def get_file(self, file_name, case_name):
        return File(open(settings.TEST_FILES_ROOT + case_name + '/' + file_name))
    
    def create_fileinfo(self, file_name, case_name):
        file_info = self.get_file(file_name, case_name)
        return FileInfo.objects.create(data_file=file_info,
                                       file_type=file_name.split('.')[0],
                                       state='pending')

    def create_admin_user(self, username="admin", password="password"):
        user = CephiaUser.objects.get_or_create(username=username, first_name='adminfirst', last_name='adminlast', is_superuser=True)[0]
        user.set_password(password)
        user.save()
        return user


class TestBase(TestCase, TestHelper):
    """ All tests should extend from this class """
    pass

