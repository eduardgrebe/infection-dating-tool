import logging
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import loader, RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
logger = logging.getLogger(__name__)
from models import Country

@login_required
def home(request, template="cephia/home.html"):
    context = {}
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def countries(request, template="cephia/countries.html"):
    context = {}
    countries = Country.objects.all().order_by("name")
    context['countries'] = countries
    return render_to_response(template, context, context_instance=RequestContext(request))
