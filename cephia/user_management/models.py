# encoding: utf-8
from lib.fields import ProtectedForeignKey
from django.contrib.auth import load_backend, login
from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from lib.models import BaseModel

import logging
logger = logging.getLogger(__name__)

class BaseUser(AbstractUser, BaseModel):
    objects = UserManager()

    class Meta:
        abstract = True

    temporary_locked_out_at = models.DateTimeField(null=True, blank=True)
    num_login_failures = models.IntegerField(default=0, null=False, blank=True)

    def on_login_failure(self):
        self.num_login_failures += 1
        if self.temporary_locked_out_at is None and self.num_login_failures > settings.MAX_NUM_FAILED_LOGINS:
            self.temporary_locked_out_at = datetime.today()
        self.save()
        return self.temporary_locked_out_at

    def is_locked_out(self):
        if self.temporary_locked_out_at is None:
            return False
        lock_expires_at = self.temporary_locked_out_at + timedelta(minutes=settings.LOCKOUT_TIME_IN_MINUTES)
        if datetime.now() > lock_expires_at:
            self.login_ok()
            return False
        else:
            return True

    def login_ok(self):
        if self.temporary_locked_out_at is None and self.num_login_failures==0:
            return
        self.temporary_locked_out_at = None
        self.num_login_failures = 0
        self.save()


class AuthenticationToken(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = ProtectedForeignKey(settings.AUTH_USER_MODEL, db_index=True, blank=False, null=False, related_name="authentication_token")
    token = models.CharField(max_length=200, blank=False, null=False, db_index=True)
    
    @classmethod
    def create_token(self, user):
        AuthenticationToken.objects.filter(user=user).delete()
        token = str(uuid.uuid4()).replace("-","").replace("_","")
        return AuthenticationToken.objects.create(user=user, token=token)

    @classmethod
    def clear_token(self, user):
        AuthenticationToken.objects.filter(user=user).delete()
        
    @classmethod
    def try_login_with_token(self, request, token):

        def override_login(request, user):
            if not hasattr(user, 'backend'):
                for backend in settings.AUTHENTICATION_BACKENDS:
                    if user == load_backend(backend).get_user(user.pk):
                        user.backend = backend
                        break
            if hasattr(user, 'backend'):
                return login(request, user)

        try:
            authtoken = AuthenticationToken.objects.get(token=token)
            override_login(request, authtoken.user)
            return True
        except AuthenticationToken.DoesNotExist:
            logger.warning("No authentication token found for %s" % token)
            return False


