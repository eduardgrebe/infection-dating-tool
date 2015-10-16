import logging
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from csv_helper import get_csv_response
from datetime import datetime, timedelta
import json
from collections import defaultdict, OrderedDict
from django.utils import timezone

logger = logging.getLogger(__name__)

@login_required
def visit_report(request, template="reporting/visit_report.html"):
    context = {}
    
    return render_to_response(template, context, context_instance=RequestContext(request))
    