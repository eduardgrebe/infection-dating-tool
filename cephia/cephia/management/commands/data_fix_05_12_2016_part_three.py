from django.core.management.base import BaseCommand, CommandError
from cephia.models import Visit, Subject, Subtype
from django.db.models import Q, F
from django.db import transaction
import logging
import traceback

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fix subtype for listed subjects.'

    def handle(self, *args, **options):
        self.fix_subject_subtypes()

    def fix_subject_subtypes(self):
        lines = [['2023037', 'BF'],
                 ['2023043', 'B'],
                 ['2023058', 'C'],
                 ['2023064', 'C'],
                 ['2023069', 'BC'],
                 ['2023077', 'B'],
                 ['2023081', 'F'],
                 ['2030001', 'B'],
                 ['2030002', 'B'],
                 ['2030009', 'B'],
                 ['2030012', 'B'],
                 ['2030014', 'B'],
                 ['2030018', 'B'],
                 ['2030023', 'B'],
                 ['2030030', 'B'],
                 ['2030033', 'B'],
                 ['2030037', 'B'],
                 ['2030041', 'B'],
                 ['2030054', 'C'],
                 ['2030059', 'BF'],
                 ['2030070', 'B']
        ]

    for i in lines:
        try:
            subtype = Subtype.objects.get(name=i[1])
        except Subtype.DoesNotExist:
            subtype = Subtype.objects.create(name=i[1])
        subject = Subject.objects.get(subject_label=i[0])
        subject.subtype = subtype
        subject.subtype_confirmed=True
        subject.save()
