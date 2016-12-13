from django import template
from django.template.loader import render_to_string
import datetime
import os

register = template.Library()

@register.simple_tag
def data_file_name(data_file_name):
    import pdb;pdb.set_trace()
    
    name = os.path.basename(data_file_name)
    return name
