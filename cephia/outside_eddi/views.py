from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from forms import EddiUserCreationForm, TestHistoryFileUploadForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from user_management.views import _check_for_login_hack_attempt
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from user_management.models import AuthenticationToken
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.views import logout as django_logout
from django.contrib.auth.models import Group
from file_handlers.outside_eddi_test_history_file_handler import TestHistoryFileHandler
from cephia.models import FileInfo

@login_required(login_url='outside_eddi:login')
def home(request, file_id=None, template="outside_eddi/home.html"):
    context = {}

    context['outside_eddi'] = True

    return render(request, template, context)

@csrf_exempt
def outside_eddi_login(request, template='outside_eddi/login.html'):
    context = {}
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()

            if user.is_locked_out():
                msg = "User %s got their login correct but is locked out so has not been allowed in. " % user.username
                messages.add_message(request, messages.WARNING, msg)
            else:
                if user.groups.filter(name=u'Outside Eddi Users').exists():
                    auth_login(request, user)
                    user.login_ok()
                    token = AuthenticationToken.create_token(user)
                    return redirect("outside_eddi:home")
                else:
                    msg = "User %s does not have the login credentials for this page so has not been allowed in. " % user.username
                    messages.add_message(request, messages.WARNING, msg)
        else:
            messages.add_message(request, messages.WARNING, "Invalid credentials")
            _check_for_login_hack_attempt(request, context)

    context['form'] = form
    return render(request, template, context)

def outside_eddi_logout(request, login_url=None, current_app=None, extra_context=None):
    if not login_url:
        login_url='outside_eddi:login'
    return django_logout(request, login_url, current_app=current_app, extra_context=extra_context)

@csrf_exempt
def outside_eddi_user_registration(request, template='outside_eddi/user_registration.html'):
    context = {}
    form = EddiUserCreationForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            return redirect("outside_eddi:home")
        else:
            messages.add_message(request, messages.WARNING, "Invalid credentials")
            _check_for_login_hack_attempt(request, context)

    context['form'] = form

    return render(request, template, context)


@login_required(login_url='outside_eddi:login')
def diagnostic_tests(request, file_id=None, template="outside_eddi/diagnostic_tests.html"):
    context = {}

    if request.method == 'POST':
        form = TestHistoryFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            latest_file = FileInfo.objects.all().last()
            
            TestHistoryFileHandler(latest_file).parse()
            TestHistoryFileHandler(latest_file).validate()
            TestHistoryFileHandler(latest_file).process()

            context['uploaded'] = 'File succesfully uploaded'
    else:
        form = TestHistoryFileUploadForm()

    context['outside_eddi'] = True
    context['form'] = form

    return render(request, template, context)
