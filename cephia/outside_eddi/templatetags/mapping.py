from django.template import Library
from outside_eddi.models import OutsideEddiDiagnosticTest

register = Library()
map_id = None

@register.simple_tag
def set_map_id(map_id):
    map_id = map_id
    return map_id

@register.simple_tag
def get_map_id():

    return map_id
