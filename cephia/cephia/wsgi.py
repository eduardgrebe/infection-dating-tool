"""
WSGI config for cephia project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys


os.environ["DJANGO_SETTINGS_MODULE"] = "cephia.settings"

PROJECT_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..")
os.environ["HOME"] = PROJECT_ROOT

sys.stdout = sys.stderr
sys.path.append(os.path.join(PROJECT_ROOT, "cephia"))
sys.path.append(os.path.join(PROJECT_ROOT, "cephia", "cephia"))
sys.path.append(os.path.join(PROJECT_ROOT, "venv","lib","python2.7","site-packages"))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
