# encoding: utf-8
import os
from lib.fields import ProtectedForeignKey
from django.contrib.auth import load_backend, login, logout
import subprocess
from django.contrib.auth import get_user_model
from django.core.files import File 
import uuid
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

