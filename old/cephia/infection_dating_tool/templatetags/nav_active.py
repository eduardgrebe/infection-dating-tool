from django.core.urlresolvers import resolve
from django.template import Library

register = Library()

@register.simple_tag
def nav_active(request, url):
    """
    In template: {% nav_active request "url_name_here" %}
    """
    url_name = resolve(request.path).view_name
    if url_name == 'residual_risk_data' \
       or url_name == 'residual_risk_estimates_calculate' \
       or url_name == 'residual_risk_estimates_specify' \
       or url_name == 'residual_risk_calculate' \
       or url_name == 'residual_risk_supply' \
       or url_name == 'residual_risk_window':
        url_name = 'residual_risk'
    if url_name == url:
        return "active"
    return "nav-eddi"
