from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

def home(request, file_id=None, template="outside_eddi/home.html"):
    context = {}

    context['welcome_message'] = 'hello'

    return render_to_response(template, context, context_instance=RequestContext(request))

# def user_registration(request, template="outside_eddi/user_registration.html"):
#     context = {}

#     context['welcome_message'] = 'hello, welcome to outside_eddit user registration'

#     return render_to_response(template, context, context_instance=RequestContext(request))
