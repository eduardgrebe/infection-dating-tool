import logging
from cephia.tests.test_base import TestBase
from cephia.models import *
from django.core.management import call_command

logger = logging.getLogger(__name__)

class TestVolumeArithmetic(TestBase):
    def setUp(self):
        super(TestVolumeArithmetic, self).setUp()

        self.transfer_ins = self.create_fileinfo('transfer_in.xlsx', 'test_case_006')
        self.aliquots = self.create_fileinfo('aliquot.xlsx', 'test_case_006')

    def test_transferin_volume_rollup(self):
        self.transfer_ins.get_handler().parse()
        self.transfer_ins.get_handler().validate()
        self.transfer_ins.get_handler().process()
        

        self.assertEqual(1, Specimen.objects.filter(specimen_label='AS10-10544').count())
        self.assertEqual(4, Specimen.objects.get(specimen_label='AS10-10544').number_of_containers)
        self.assertEqual(10000, Specimen.objects.get(specimen_label='AS10-10544').initial_claimed_volume)

    def test_transferin_multicontainer_volume(self):
        self.transfer_ins.get_handler().parse()
        self.transfer_ins.get_handler().validate()
        self.transfer_ins.get_handler().process()

        self.assertEqual(1, Specimen.objects.filter(specimen_label='AS10-10545').count())
        self.assertEqual(4, Specimen.objects.get(specimen_label='AS10-10545').number_of_containers)
        self.assertEqual(4000, Specimen.objects.get(specimen_label='AS10-10545').initial_claimed_volume)

    def test_transferin_rollup_and_multicontainer_volume(self):
        self.transfer_ins.get_handler().parse()
        self.transfer_ins.get_handler().validate()
        self.transfer_ins.get_handler().process()

        self.assertEqual(1, Specimen.objects.filter(specimen_label='AS10-10546').count())
        self.assertEqual(5, Specimen.objects.get(specimen_label='AS10-10546').number_of_containers)
        self.assertEqual(4600, Specimen.objects.get(specimen_label='AS10-10546').initial_claimed_volume)

    def test_aliquot_volume_update(self):
        self.transfer_ins.get_handler().parse()
        self.transfer_ins.get_handler().validate()
        self.transfer_ins.get_handler().process()
        self.aliquots.get_handler().parse()
        self.aliquots.get_handler().validate()
        self.aliquots.get_handler().process()

        self.assertEqual(1, Specimen.objects.filter(specimen_label='AS10-10544').count())
        self.assertEqual(10000, Specimen.objects.get(specimen_label='AS10-10544').initial_claimed_volume)
        self.assertEqual(8500, Specimen.objects.get(specimen_label='AS10-10544').volume)
        self.assertEqual(250, Specimen.objects.get(specimen_label='1234-01').volume)
