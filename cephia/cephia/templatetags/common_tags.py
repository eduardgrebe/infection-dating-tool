from django import template

register = template.Library()
import logging
logger = logging.getLogger(__name__)

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg
