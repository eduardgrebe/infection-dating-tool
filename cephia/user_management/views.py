import logging

from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth.views import logout as django_logout
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm

from api import api
from api.decorators import api_login_required, fix_ssl_url
from forms import (
    UserEditForm, HRUserEditForm, UserProfileForm, 
    GroupEditForm, LoginForm, ActivateUserForm
)
logger = logging.getLogger(__name__)

def login(request, template="admin/login.html", redirect_field_name='next'):
    context = {}

    form = AuthenticationForm(request, data=request.POST)
    if request.POST:
        if form.is_valid():

            redirect_to = request.REQUEST.get(redirect_field_name, None)
            if not redirect_to:
                redirect_to = request.GET.get(redirect_field_name, '')
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            user = form.get_user()

            if user.is_locked_out():
                msg = "User %s got their login correct but is locked out so has not been allowed in. " % user.username
                logger.warning(msg)
                context['status'] = 'failed'
                context['error_msg'] = "This account is locked"
            if not user.is_staff:
                msg = "User is not a staff user, login disabled"
                logger.warning(msg)
                context['status'] = 'failed'
                context['error_msg'] = "This account may not login"
            else:
                auth_login(request, user)
                user.login_ok()
                return HttpResponseRedirect(redirect_to)

        else:
            context['status'] = 'failed'
            context['error_msg'] = "Invalid credentials"
            _check_for_login_hack_attempt(request, context)
    
    return render_to_response(template, context, context_instance=RequestContext(request))


def _check_for_login_hack_attempt(request, context):
    if request.POST.get('username'):
        try:
            user = get_user_model().objects.get(username=request.POST.get('username'))
        except get_user_model().DoesNotExist:
            return
        if user.is_locked_out():
            msg = "Failed login attempt on an already locked out user : %s" % user.username
            logger.warning(msg)
            context['error_msg'] = "This account is locked"
            
        if user.on_login_failure():
            logger.warning("Locking for Repeated login failure: %s has been locked out" % user.username)
            context['error_msg'] = "This account has been locked"

def logout(request, login_url=None, current_app=None, extra_context=None):
    if not login_url:
        login_url = settings.LOGIN_URL
    login_url = resolve_url(login_url)
    login_url = fix_ssl_url(request, login_url)
    return django_logout(request, login_url, current_app=current_app, extra_context=extra_context)
