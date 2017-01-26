from django.core.management.base import BaseCommand, CommandError
from cephia.models import Subject
from django.db.models import F
import logging
import random

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Updating any previous Subjects which do not yet have the subject_label_blinded field populated'

    def handle(self, *args, **options):
        subjects = Subject.objects.filter(subject_label_blinded__isnull=True)
        
        for subject in subjects:
            import pdb;pdb.set_trace()
            subject_id = subject.pk
            random.seed(subject_id)
            new_subject_id = random.random()
            
