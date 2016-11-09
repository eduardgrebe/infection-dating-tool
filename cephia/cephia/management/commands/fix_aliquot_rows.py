from django.core.management.base import BaseCommand, CommandError
from diagnostics.models import DiagnosticTestHistory, TestPropertyEstimate
from cephia.models import AliquotRow
import logging

logger = logging.getLogger(__name__)

tasks = [['change parent ID', '4760-06', 119240],
         ['change parent ID', '6232-05', 119245],
         ['change parent ID', '1992-06', 119250],
         ['change parent ID', '5187-05', 119255],
         ['change parent ID', '9089-05', 119260],
         ['change parent ID', '2133-05', 119265],
         ['change volume', 100, 119278],
         ['change volume', 150, 119298],
         ['change volume', 50, 119338],
         ['change volume', 100, 119343],
         ['change volume', 75, 119358],
         ['change volume', 100, 119363],
         ['change volume', 100, 119368],
         ['change volume', 100, 119373],
         ['change volume', 100, 119383],
         ['change volume', 50, 119386],
         ['change volume', 75, 119389],
         ['change volume', 100, 119392],
         ['delete', '', 119241],
         ['delete', '', 119242],
         ['delete', '', 119243],
         ['delete', '', 119246],
         ['delete', '', 119247],
         ['delete', '', 119248],
         ['delete', '', 119251],
         ['delete', '', 119252],
         ['delete', '', 119253],
         ['delete', '', 119256],
         ['delete', '', 119257],
         ['delete', '', 119258],
         ['delete', '', 119261],
         ['delete', '', 119262],
         ['delete', '', 119263],
         ['delete', '', 119266],
         ['delete', '', 119267],
         ['delete', '', 119268]]

class Command(BaseCommand):
    help = 'fixing aliquot rows'

    def handle(self, *args, **options):
        for task in tasks:
            if task[0] == 'change parent ID':
                ali = AliquotRow.objects.get(pk=task[2])
                ali.parent_label = task[1]
                ali.save()
            elif task[0] == 'change volume':
                ali = AliquotRow.objects.get(pk=task[2])
                ali.volume = task[1]
                ali.save()
            elif task[0] == 'delete':
                if AliquotRow.objects.filter(pk=task[2]).exists():
                    ali = AliquotRow.objects.get(pk=task[2]).delete()

        logger.info('Successfully fixed aliquote rows')
