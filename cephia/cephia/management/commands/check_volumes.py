from django.core.management.base import BaseCommand, CommandError
from cephia.file_handlers.file_handler import FileHandler
from datetime import datetime, date
from cephia.file_handlers.handler_imports import *
from cephia.models import TransferInRow, Specimen, SpecimenType
from django.db import connection
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Check all specimen label/specimen type sets to confirm that the volumes are as expected and provide a list of any which have unexpected volumes or had an error for one or more bellow the line rows'

    def handle(self, *args, **options):
        specimens = Specimen.objects.all()

        spec_label_type = specimens.values('id', 'specimen_label', 'specimen_type__spec_type').distinct()

        errors = {}
        
        for spec in spec_label_type:
            rows = TransferInRow.objects.filter(specimen_label=spec['specimen_label'], specimen_type=spec['specimen_type__spec_type'])
            error_msgs = ''

            volume_count = 0
            container_count = 0
            
            for row in rows:
                containers = int(row.number_of_containers)
                volume = float(row.volume) * containers
                volume_count = volume_count + volume
                container_count = container_count + containers

                if row.state == 'error':
                    error_msgs += 'Below the line id: %s, specimen_label: %s, Error message: %s' % (row.id, row.specimen_label, row.error_message)


            specimen = Specimen.objects.get(id=spec['id'])
            if specimen.volume != volume_count:
                error_msgs += 'Specimen: %s, Volume: %s.\n' % (specimen.id, specimen.volume)
                error_msgs += 'Below the lines total volume: %s.\n' % volume_count
            if specimen.number_of_containers != container_count:
                error_msgs += 'Specimen: %s, Container count: %s.\n' % (specimen.id, specimen.number_of_containers)
                error_msgs += 'Below the lines total containers: %s.\n' % container_count

            if error_msgs:
                errors[spec['id']] = error_msgs
                print errors[spec['id']]

