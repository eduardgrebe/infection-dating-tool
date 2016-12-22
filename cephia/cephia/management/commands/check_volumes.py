from django.core.management.base import BaseCommand, CommandError
from cephia.file_handlers.file_handler import FileHandler
from datetime import datetime, date
from cephia.file_handlers.handler_imports import *
from cephia.models import TransferInRow, Specimen, SpecimenType
from django.db import connection
import logging
import csv
from cephia.settings import BASE_DIR

logger = logging.getLogger(__name__)

outfile_path = '%s/volume_log.csv' % BASE_DIR

class Command(BaseCommand):
    help = 'Check all specimen label/specimen type sets to confirm that the volumes are as expected and provide a list of any which have unexpected volumes or had an error for one or more bellow the line rows'

    def handle(self, *args, **options):
        specimens = Specimen.objects.all()
        spec_label_type = specimens.values('id', 'specimen_label', 'specimen_type', 'specimen_type__spec_type', 'volume', 'number_of_containers').distinct()

        errors = {}

        for spec in spec_label_type:
            rows = TransferInRow.objects.filter(specimen_label=spec['specimen_label'], specimen_type=spec['specimen_type__spec_type'])
            row_details = rows.values('id', 'number_of_containers', 'volume', 'state', 'error_message', 'specimen_type')

            error_msgs = {}
            volume_count = 0
            container_count = 0

            for row in row_details:
                try:
                    row_containers = int(row['number_of_containers'])
                except TypeError:
                    row_containers = 0
                try:
                    row_volume = float(row['volume'])
                except TypeError:
                    row_volume = 0

                volume = row_volume * row_containers
                volume_count = volume_count + volume
                container_count = container_count + row_containers

                if row['state'] == 'error':
                    if 'Below the line error msg' not in error_msgs:
                        error_msgs['Below the line error msg'] = []
                    error_msgs['Below the line error msg'].append('Below the line id: %s, Error message: %s' % (row['id'], row['error_message']))


            try:
                spec_volume = float(spec['volume'])
            except TypeError:
                spec_volume = 'None'
            try:
                spec_number_of_containers = int(spec['number_of_containers'])
            except TypeError:
                spec_number_of_containers = 'None'

            if spec_volume != volume_count:
                error_msgs['Specimen volume'] = spec_volume
                
                if row_details:
                    error_msgs['Below the Lines total volume'] = volume_count or 'None'
                    error_msgs['Below the Lines volumes'] = [ x['volume'] or 'None' for x in row_details ]
                else:
                    error_msgs['Info'] = 'no transfer in rows found for specimen label: %s, specimen_type: %s' % (
                        spec['specimen_label'],
                        spec['specimen_type__spec_type']
                    )
                    
            if spec_number_of_containers != container_count:
                error_msgs['Specimen containers'] = spec_number_of_containers
                
                if row_details:
                    error_msgs['Below the Lines total containers'] = container_count or 'None'
                    error_msgs['Below the Lines containers'] = [ x['number_of_containers'] or 'None' for x in row_details ]
                else:
                    error_msgs['Info'] = 'no transfer in rows found for specimen label: %s, specimen_type: %s' % (
                        spec['specimen_label'],
                        spec['specimen_type__spec_type']
                    )

            if error_msgs:
                error_msgs['Specimen label'] = spec['specimen_label']
                error_msgs['Specimen type'] = spec['specimen_type__spec_type']
                error_msgs['Below the line specimen types'] = [ x['specimen_type'] for x in row_details ]
                errors[spec['id']] = error_msgs

        dump(errors, outfile_path)


def dump(errors, outfile_path):
    writer = csv.writer(open(outfile_path, 'w'))

    headers = ['Specimen id', 'Specimen label', 'Below the line specimen types', 'Specimen type', 'Below the line error msg', 'Specimen volume', 'Below the Lines total volume', 'Below the Lines volumes', 'Specimen containers', 'Below the Lines total containers', 'Below the Lines containers', 'Info']
    writer.writerow(headers)

    for error in errors:
        row = []
        row.append(error)
        
	for header in headers:
            if header == 'Specimen id':
                continue
            try:
	        row.append(errors[error][header])
            except KeyError:
                row.append('')

	writer.writerow(row)
