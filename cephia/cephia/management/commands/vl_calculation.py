from django.core.management.base import BaseCommand, CommandError
from cephia.models import Visit, Subject
from django.db.models import Q, F
from django.db import transaction
import logging
import traceback

logger = logging.getLogger(__name__)

def vl_as_int(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        value = None
    return value

class Command(BaseCommand):
    help = 'Update viral load data for all visits'

    def handle(self, *args, **options):
        self.update_source_study_viral_loads()
        self.update_cephia_viral_loads()

    def update_cephia_viral_loads(self):
        upper_limit = Visit.objects.filter(vl_cephia__isnull=False, vl_cephia__startswith='<')
        lower_limit = Visit.objects.filter(vl_cephia__isnull=False, vl_cephia__startswith='>')
        quantitative = Visit.objects.filter(vl_cephia__isnull=False)\
                                    .exclude(pk__in=[ visit.id for visit in upper_limit ])\
                                    .exclude(pk__in=[ visit.id for visit in lower_limit ])

        self.update_viral_loads(upper_limit, lower_limit, quantitative, 'vl_cephia')
        
    def update_source_study_viral_loads(self):
        upper_limit = Visit.objects.filter(vl_reported__isnull=False, vl_reported__startswith='<')
        lower_limit = Visit.objects.filter(vl_reported__isnull=False, vl_reported__startswith='>')
        quantitative = Visit.objects.filter(vl_reported__isnull=False)\
                                    .exclude(pk__in=[ visit.id for visit in upper_limit ])\
                                    .exclude(pk__in=[ visit.id for visit in lower_limit ])

        self.update_viral_loads(upper_limit, lower_limit, quantitative)

    def update_viral_loads(self, upper_limit, lower_limit, quantitative, field='vl_reported'):
        with transaction.atomic():
            for visit in quantitative:
                try:
                    vl = getattr(visit, field)
                    if vl.startswith('='):
                        value = vl[1:]
                    else:
                        value = vl

                    visit.viral_load = vl_as_int(value)
                    visit.vl_detectable = True
                    visit.vl_type = 'quantitative'
                    visit.viral_load_offset = 0
                    visit.save()
                except Exception, e:
                    traceback.print_exc()
                    break

        with transaction.atomic():
            for visit in upper_limit:
                try:
                    vl_reported = getattr(visit, field)
                    visit.viral_load = vl_as_int(vl_reported[1:])
                    visit.vl_detectable = False
                    visit.vl_type = 'upper_limit'
                    visit.viral_load_offset = 0
                    visit.save()
                except Exception, e:
                    traceback.print_exc()
                    break
                    

        with transaction.atomic():
            for visit in lower_limit:
                try:
                    vl_reported = getattr(visit, field)
                    visit.viral_load = vl_as_int(vl_reported[1:])
                    visit.vl_detectable = True
                    visit.vl_type = 'lower_limit'
                    visit.viral_load_offset = 0
                    visit.save()
                except Exception, e:
                    traceback.print_exc()
                    break

    def find_nearby_viral_loads():
        with transaction.atomic():
            visits = Visit.Objects.filter(viral_load=None)
            for visit in visits:
                visit.find_nearby_viral_load()
                
