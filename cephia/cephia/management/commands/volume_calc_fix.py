from django.core.management.base import BaseCommand, CommandError
from cephia.file_handlers.file_handler import FileHandler
from datetime import datetime, date
from cephia.file_handlers.handler_imports import *
from cephia.models import TransferInRow
from django.db import connection
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Recalculate volume from below the line and push result above the line'

    def dictfetchall(self, cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    def handle(self, *args, **options):
        rows = TransferInRow.objects.filter(state='processed', roll_up=False)

        roll_up_sql = """
        SELECT
        specimen_label,
        specimen_type,
        SUM(volume * number_of_containers) as actual_volume,
        SUM(number_of_containers) as number_of_containers,
        SUM(volume) as volume,
        MAX(transfer_date_dd) as transfer_date_dd,
        MAX(transfer_date_mm) as transfer_date_mm,
        MAX(transfer_date_yyyy) as transfer_date_yyyy,
        MAX(drawdate_yyyy) as drawdate_yyyy,
        MAX(drawdate_mm) as drawdate_mm,
        MAX(drawdate_dd) as drawdate_dd,
        MAX(subject_label) as subject_label,
        MAX(location) as location,
        MAX(transfer_reason) as transfer_reason,
        MAX(volume_units) as volume_units,
        MAX(source_study) as source_study
        FROM cephia_transfer_in_rows
        WHERE state='processed'
        AND roll_up = 1
        GROUP BY specimen_label, specimen_type;
        """

        cursor = connection.cursor()
        cursor.execute(roll_up_sql)

        rows_roll_up = self.dictfetchall(cursor)

        for row in rows:
            row.specimen.initial_claimed_volume = (float(row.volume) * float(row.number_of_containers))

        for row in rows_roll_up:
            row.specimen.initial_claimed_volume = float(row['actual_volume'])

        logger.info('Success!')
