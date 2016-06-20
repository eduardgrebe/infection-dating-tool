from django.core.management.base import BaseCommand, CommandError
from cephia.models import Visit, Subject
from django.db.models import Q, F
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update viral load data for all visits'

    def handle(self, *args, **options):
        upper_limit = Visit.objects.filter(vl_reported__isnull=False, vl_reported__startswith='<')
        lower_limit = Visit.objects.filter(vl_reported__isnull=False, vl_reported__startswith='>')
        quantitative = Visit.objects.filter(vl_reported__isnull=False)\
                                    .exclude(pk__in=[ visit.id for visit in upper_limit ])\
                                    .exclude(pk__in=[ visit.id for visit in lower_limit ])
        with transaction.atomic():
            for visit in quantitative:
                try:
                    if visit.vl_reported.startswith('='):
                        visit.viral_load = visit.vl_reported[1:]
                    else:
                        visit.viral_load = visit.vl_reported

                    visit.vl_detectable = True
                    visit.vl_type = 'quantitative'
                    visit.save()
                except Exception, e:
                    continue

        with transaction.atomic():
            for visit in upper_limit:
                try:
                    visit.viral_load = visit.vl_reported[1:]
                    visit.vl_detectable = False
                    visit.vl_type = 'upper_limit'
                    visit.save()
                except Exception, e:
                    continue

        with transaction.atomic():
            for visit in lower_limit:
                try:
                    visit.viral_load = visit.vl_reported[1:]
                    visit.vl_detectable = True
                    visit.vl_type = 'lower_limit'
                    visit.save()
                except Exception, e:
                    continue
