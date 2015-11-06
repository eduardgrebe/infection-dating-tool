import os
from collections import namedtuple
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.shortcuts import render_to_response, redirect
from django.db.models import Sum, Count, Q, F, Max, Min
from django.contrib import messages
from django.template import RequestContext
from django.views import i18n
from django.conf import settings
from django.contrib import messages
from django.utils import translation
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, get_user_model
from django.contrib.auth.views import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.sites.models import get_current_site
from django.utils.http import base36_to_int, is_safe_url, urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import resolve_url
from django_remote_forms.forms import RemoteForm
from django.forms.models import model_to_dict
from django.template.loader import render_to_string

from ssl_decorators import fix_ssl_url
from mailqueue.mailqueue_helper import queue_admin_email, queue_email

from api.decorators import copy_json_to_post, token_login
from api import api
from forms import UserEditForm, UserProfileForm, GroupEditForm, ActivateUserForm
import datetime
from core.models import *
from user_management.models import AuthenticationToken

import logging
logger = logging.getLogger(__name__)

@csrf_exempt
@copy_json_to_post
def is_logged_in(request):
    context = {}
    if api.token_login(request):
        api.set_response_ok(context)
    else:
        api.set_response_fail(context, 'Not logged in')
    return HttpResponse(api.dump_for_response(context))

@csrf_exempt
@copy_json_to_post
def login(request):
    context = {}

    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():

        user = form.get_user()

        if user.is_locked_out():
            msg = "User %s got their login correct but is locked out so has not been allowed in. " % user.username
            logger.warning(msg)
            queue_admin_email("User login on a locked out account", msg)
            context['status'] = 'failed'
            context['error_msg'] = "This account is locked"
        else:
            auth_login(request, user)
            user.login_ok()
            token = AuthenticationToken.create_token(user)

            context['api_token'] = token.token
            context['user'] = user.model_to_dict()
            context['status'] = 'ok'
    else:
        context['status'] = 'failed'
        context['error_msg'] = "Invalid credentials"
        _check_for_login_hack_attempt(request, context)

    return HttpResponse(api.dump_for_response(context))

def _check_for_login_hack_attempt(request, context):
    if request.POST.get('username'):
        try:
            user = get_user_model().objects.get(username=request.POST.get('username'))
        except get_user_model().DoesNotExist:
            return
        if user.is_locked_out():
            msg = "Failed login attempt on an already locked out user : %s" % user.username
            logger.warning(msg)
            queue_admin_email(subject="Locked account login failure: %s is already locked out" % user.username, 
                             msg="Number of login failures: %d. Locked out at %s" % (user.num_login_failures, user.temporary_locked_out_at))
            context['error_msg'] = "This account is locked"
            
        if user.on_login_failure():
            logger.warning("Locking for Repeated login failure: %s has been locked out" % user.username)
            queue_admin_email(subject="Locking for Repeated login failure: %s has been locked out" % user.username, 
                             msg="Number of login failures: %d. Locked out at %s" % (user.num_login_failures, user.temporary_locked_out_at))
            context['error_msg'] = "This account has been locked"

def logout(request, login_url=None, current_app=None, extra_context=None):
    if not login_url:
        login_url = settings.LOGIN_URL
    login_url = resolve_url(login_url)
    login_url = fix_ssl_url(request, login_url)
    return django_logout(request, login_url, current_app=current_app, extra_context=extra_context)

@csrf_exempt
@copy_json_to_post
@token_login
@user_passes_test(lambda u: u.is_superuser or u.has_perm("riley.add_users"))
def user_list(request):
    context = {}

    try:
        users = get_user_model().objects.all().order_by("username")

        api.set_response_ok(context)

        flattened_users = list(users.values())

        context = { 'data' : { 'users' : flattened_users,
                               'user_count': users.count() },
                    'errors' : [] }
    except Exception, ex:
        logger.exception(ex)
        api.set_response_fail(context, str(ex))

    return HttpResponse(api.dump_for_response(context))

@csrf_exempt
@copy_json_to_post
@token_login
@user_passes_test(lambda u: u.is_superuser or u.has_perm("riley.send_email") or u.has_perm('riley.add_users'))
def unactivated_users(request):
    context = {}
    try:
        users = get_user_model().objects.filter(
            send_activation_email=True, 
            activation_key__isnull=False,
            activation_key_expires__gte=api.normalized_today()
        )

        api.set_response_ok(context)

        flattened_users = list(users.values())

        context = { 'data' : { 'users' : flattened_users,
                               'user_count': users.count() },
                    'errors' : [] }
    except Exception, ex:
        logger.exception(ex)
        api.set_response_fail(context, str(ex))

    return HttpResponse(api.dump_for_response(context))

@csrf_exempt
@copy_json_to_post
@token_login
@user_passes_test(lambda u: u.is_superuser or u.has_perm("riley.add_users"))
def user_add(request, template="user_management/user_add.html"):
    context = { 'data': {} }

    try:
        if request.method == 'POST':
            form = UserEditForm(request.POST or None)
            if form.is_valid():
                user = form.save()
                api.set_response_ok(context)
            else:
                api.set_response_fail(context, "Form is not valid : %s" % form.errors)
            remote_form = RemoteForm(form)
            context.update(remote_form.as_dict())
        else:
            context['data']['groups'] = [model_to_dict(x) for x in Group.objects.all().order_by("name")]
            context['data']['languages'] = [model_to_dict(x) for x in Language.objects.all().order_by("language_name")]
            api.set_response_ok(context)
    except Exception, ex:
        logger.exception(ex)
        api.set_response_fail(context, str(ex))

    return HttpResponse(api.dump_for_response(context))

@csrf_exempt
@copy_json_to_post
@token_login
@user_passes_test(lambda u: u.is_superuser)
def user_edit(request):
    context = { 'data': {} }

    try:
        if request.method == 'POST':
            user_id = request.POST['user_id']
            user = get_user_model().objects.get(pk=user_id)

            form = UserEditForm(request.POST or None, instance=user)
            if form.is_valid():
                user = form.save()
                api.set_response_ok(context)
            else:
                api.set_response_fail(context, "Form is not valid : %s" % form.errors)
            remote_form = RemoteForm(form)
            context.update(remote_form.as_dict())
        else:
            user_id = request.DATA['user_id']
            user = get_user_model().objects.get(pk=user_id)

            context['data']['user'] = user_profile_to_dict(user)
            context['data']['groups'] = [model_to_dict(x) for x in Group.objects.all().order_by("name")]
            context['data']['languages'] = [model_to_dict(x) for x in Language.objects.all().order_by("language_name")]
            api.set_response_ok(context)

    except Exception, ex:
        logger.exception(ex)
        api.set_response_fail(context, str(ex))

    return HttpResponse(api.dump_for_response(context))


@csrf_exempt
@copy_json_to_post
@token_login
def user_profile(request):
    context = { 'data': {} }
    user = request.user
    try:
        if request.method == 'POST':
            form = UserProfileForm(request.POST or None, instance=user)

            if form.is_valid():
                user = form.save()
                api.set_response_ok(context)
            else:
                api.set_response_fail(context, "Form is not valid")
            
            remote_form = RemoteForm(form)
            context.update(remote_form.as_dict())
            context['data']['user'] = user_profile_to_dict(user)
        else:
            context['data']['user'] = user_profile_to_dict(user)
            context['data']['landing_pages'] = []
            context['data']['languages'] = [model_to_dict(x) for x in Language.objects.all().order_by("language_name")]
    
            for x in user.groups.order_by("name"):
                landing_page = x.allowed_landing_pages.first()
                if landing_page:
                    context['data']['landing_pages'].append(model_to_dict(landing_page))
            
            api.set_response_ok(context)
    except Exception, ex:
        logger.exception(ex)
        api.set_response_fail(context, str(ex))

    return HttpResponse(api.dump_for_response(context))

@csrf_exempt
@copy_json_to_post
@token_login
@user_passes_test(lambda u: u.is_superuser)
def group_list(request):
    context = { 'data': {} }

    groups = Group.objects.all().order_by("name")
    context['data']['groups'] = [model_to_dict(g) for g in groups]
    context['data']['group_count'] = groups.count()

    return HttpResponse(api.dump_for_response(context))

@csrf_exempt
@copy_json_to_post
@token_login
@user_passes_test(lambda u: u.is_superuser)
def group_add(request, template="user_management/group_add.html"):
    context = {}
    form = GroupEditForm(request.POST or None)
    if form.is_valid():
        group = form.save()
        messages.add_message(request, messages.INFO, _('New group created : %s') % group.name)
        return HttpResponseRedirect(fix_ssl_url(request, reverse('users:group_list')))
    context['form'] = form
    return render_to_response(template, context, context_instance=RequestContext(request))

@csrf_exempt
@copy_json_to_post
@token_login
@user_passes_test(lambda u: u.is_superuser)
def group_edit(request):
    context = { 'data': {}, 'errors': {}, 'messages': [] }

    try:
        if request.method == 'POST':
            group_id = request.POST['group_id']
            group = Group.objects.get(pk=group_id)

            form = GroupEditForm(request.POST or None, instance=group)

            if form.is_valid():
                group = form.save()
                api.set_response_ok(context)
            else:
                api.set_response_fail(context, "Form is not valid : %s" % form.errors)

            remote_form = RemoteForm(form)
            context.update(remote_form.as_dict())
        else:
            group_id = request.DATA['group_id']
            group = Group.objects.get(pk=group_id)

            context['data']['group'] = model_to_dict(group)
            permissions = Permission.objects.all().exclude(name__contains="Can add").exclude(name__contains="Can delete").exclude(name__contains="Can change").order_by("name")

            context['data']['permissions'] = [model_to_dict(p) for p in permissions]
            api.set_response_ok(context)

    except Exception, ex:
        logger.exception(ex)
        api.set_response_fail(context, str(ex))

    return HttpResponse(api.dump_for_response(context))


@csrf_exempt
@copy_json_to_post
def activate_user(request):
    activation_key = request.POST.get('activation_key')
    context = {}
    now = api.normalized_today()
    try:
        user = RileyUser.objects.get(activation_key=activation_key)
    except RileyUser.objects.DoesNotExist:
        api.set_response_fail(context, "No user found with the specified activation key")
    else: 
        if (now - user.activation_key_expires).days > settings.ACTIVATION_KEY_LIFESPAN_DAYS:
            api.set_response_fail(context, "Activation key has expired")
        else:
            form = ActivateUserForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save(user)
                api.set_response_ok(context)
            else:
                api.set_response_fail(context, "Could not set password", form.errors)

    return HttpResponse(api.dump_for_response(context))
    
@csrf_exempt
@copy_json_to_post
def check_activation_key(request):
    activation_key = request.DATA.get('activation_key')
    context = {}
    now = api.normalized_today()
    try:
        user = RileyUser.objects.get(activation_key=activation_key, activation_key_expires__isnull=False)
    except RileyUser.DoesNotExist:
        api.set_response_fail(context, "No user found with the specified activation key")
    else: 
        if (now - user.activation_key_expires).days > settings.ACTIVATION_KEY_LIFESPAN_DAYS:
            api.set_response_fail(context, "Activation key has expired")
        else:
            api.set_response_ok(context)

    return HttpResponse(api.dump_for_response(context))
    
@csrf_exempt
@copy_json_to_post
@token_login
@user_passes_test(lambda u: u.is_superuser)
def generate_activation_key(request):
    user_id = request.POST.get('user_id')
    context = {}
    try:
        user = RileyUser.objects.get(pk=user_id)
    except RileyUser.DoesNotExist:
        api.set_response_fail(context, "User does not exist")
    else:
        user.generate_activation_key()
        user.save()
        context['activation_key'] = user.activation_key
        api.set_response_ok(context)
    return HttpResponse(api.dump_for_response(context))    

@csrf_exempt
@copy_json_to_post
@token_login
@user_passes_test(lambda u: u.is_superuser or u.has_perm('riley.send_activation_mail'))
def send_activation_email(request):
    context = {}
    try:
        try:
            user = RileyUser.objects.get(pk=request.POST['user_id'])
        except RileyUser.DoesNotExist:
            api.set_response_fail(context, "User does not exist")
            HttpResponse(api.dump_for_response(context))    

        if not user.activation_key:
            api.set_response_fail(context, "User already activated")
            return HttpResponse(api.dump_for_response(context))    

        queue_email(
            request.POST['subject'],
            request.POST['text_content'],
            request.POST['html_content'],
            [user.email],
        )
        user.send_activation_email = False
        user.save()
        api.set_response_ok(context)
    except Exception, ex:
        logger.exception(ex)
        api.set_response_fail(context, str(ex))

    return HttpResponse(api.dump_for_response(context))
