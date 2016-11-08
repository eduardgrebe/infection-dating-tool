from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import messages
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.views import logout as django_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import resolve_url
from forms import UserEditForm, UserCreationForm
from user_management.models import AuthenticationToken
from django.core.urlresolvers import reverse

import logging
logger = logging.getLogger(__name__)


@csrf_exempt
def login(request, template='admin/cephia_login.html'):
    context = {}
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()

            if user.is_locked_out():
                msg = "User %s got their login correct but is locked out so has not been allowed in. " % user.username
                messages.add_message(request, messages.WARNING, msg)
            elif user.groups.filter(name=u'Outside Eddi Users').exists():
                msg = "User %s does not have the login credentials for this page so has not been allowed in. " % user.username
                messages.add_message(request, messages.WARNING, msg)
            else:
                auth_login(request, user)
                user.login_ok()
                token = AuthenticationToken.create_token(user)
                return HttpResponseRedirect(reverse("home"))
        else:
            messages.add_message(request, messages.WARNING, "Invalid credentials")
            _check_for_login_hack_attempt(request, context)

    context['form'] = form
    return render_to_response(template, context, context_instance=RequestContext(request))

def _check_for_login_hack_attempt(request, context):
    if request.POST.get('username'):
        try:
            user = get_user_model().objects.get(username=request.POST.get('username'))
        except get_user_model().DoesNotExist:
            return
        if user.is_locked_out():
            msg = "Failed login attempt on an already locked ouuser : %s" % user.username
            logger.warning(msg)
            messages.add_message(request, messages.INFO, msg)
            
        if user.on_login_failure():
            logger.warning("Locking for Repeated login failure: %s has been locked out" % user.username)
            messages.add_message(request, messages.INFO, "This account has been locked")


def logout(request, login_url=None, current_app=None, extra_context=None):
    if not login_url:
        login_url = settings.LOGIN_REDIRECT_URL
    return django_logout(request, login_url, current_app=current_app, extra_context=extra_context)


@csrf_exempt
@user_passes_test(lambda u: u.is_superuser)
def user_list(request, template="user_management/user_list.html"):
    context = {}
    try:
        users = get_user_model().objects.all().order_by("username")
        flattened_users = list(users.values())
        context = {'users' : flattened_users,
                   'user_count': users.count() }
    except Exception, ex:
        logger.exception(ex)

    return render_to_response(template, context, context_instance=RequestContext(request))

@csrf_exempt
@user_passes_test(lambda u: u.is_superuser)
def user_add(request, template="user_management/user_add.html"):
    context = {}
    try:
        form = UserEditForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                user = form.save()
                messages.add_message(request, messages.SUCCESS, "User created")
            else:
                messages.add_message(request, messages.WARNING, "Form is not valid : %s" % form.errors)
            return HttpResponseRedirect(reverse("users:user_list"))
        else:
            context['groups'] = [ x for x in Group.objects.all().order_by("name")]
    except Exception, ex:
        logger.exception(ex)
        messages.add_message(request, messages.ERROR, ex)

    context['form'] = form
    return render_to_response(template, context, context_instance=RequestContext(request))

@csrf_exempt
@user_passes_test(lambda u: u.is_superuser)
def user_edit(request, user_id=None, template="user_management/user_edit.html"):
    context = {}
    try:
        user = get_user_model().objects.get(pk=user_id)
        form = UserEditForm(request.POST or None, instance=user)

        if request.method == "POST":
            if form.is_valid():
                user = form.save()
            else:
                messages.add_message(request, messages.INFO, "Failed to edit user")

            return HttpResponseRedirect(reverse("users:user_list"))
        context['form'] = form
    except Exception, ex:
        logger.exception(ex)
        messages.add_message(request, messages.WARNING, ex)

    return render_to_response(template, context, context_instance=RequestContext(request))
