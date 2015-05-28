# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

import os
import git
import sys
from django.conf import global_settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))

LOG_FOLDER=os.path.join(PROJECT_HOME, "..", "..", 'logs')
LOG_FILENAME="cephia.log"
LOG_LEVEL="INFO"

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/users/login"
REVISION = git.Repo(os.path.join(PROJECT_HOME, "..", "..")).head.commit.hexsha

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%ikqh(&mt)5&$t^h19eb2o5g^^hbrx2i(_cby$(48xcd00_61v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = "cephia.CephiaUser"

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_HOME, "templates"),
)

ENDLESS_PAGINATION_PER_PAGE=20
ENDLESS_PAGINATION_ADD_NOFOLLOW=True #from endless docs: Set to True if your SEO alchemist wants search engines not to follow pagination links.


SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_TIMEOUT_MINUTES = 999999
SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"

# used in paranoidsessions/django-crossdomainxhr-middleware.py for Access-Control-Allow-Origin
URL_PREFIX = ''

PSESSION_NONCE_TIMEOUT = None
PSESSION_SESSION_KEY = "PARANOID_SESSION_DATA"
PSESSION_CHECK_HEADERS = ("REMOTE_ADDR","HTTP_X_FORWARDED_FOR","HTTP_USER_AGENT",)
PSESSION_NONCE_WINDOW = 1
PSESSION_NONCE_WINDOW_TIMEOUT = 1
PSESSION_KEY_TIMEOUT = None
PSESSION_SESSION_KEY = "PARANOID_SESSION_DATA"
PSESSION_COOKIE_NAME = "sessionnonce"
PSESSION_HEADER_HASH_SESSION_NAME = "psessionheaderhash"
PSESSION_SECURE_COOKIE_NAME = "sessionid_https"
PSESSION_COOKIE_HTTPONLY = True
PSESSION_REQUEST_FILTER_FUNCTION = lambda req: True
PSESSION_CLEAR_SESSION_FUNCTION = lambda req: req.session.flush()

XS_SHARING_ALLOWED_ORIGINS = '*'
XS_SHARING_ALLOWED_METHODS = ['GET','OPTIONS']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'paranoidsessions',

    'cephia',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'paranoidsessions.ParanoidSessionMiddleware',
    'paranoidsessions.csrf_middleware.HttpOnlyCsrf',
    'paranoidsessions.django-crossdomainxhr-middleware.XsSharing',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
)

ROOT_URLCONF = 'cephia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
)

WSGI_APPLICATION = 'cephia.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "Africa/Johannesburg"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'+REVISION+'/'
STATIC_ROOT = os.path.join(PROJECT_HOME, '..', '..', 'static_collected', REVISION)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_HOME, '..', '..', 'media')

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(LOG_FOLDER, "email")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(process)d %(asctime)s %(module)s.%(funcName)s[%(lineno)d]: %(message)s'
            },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
            },
        },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
            },
        'file':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':os.path.join(LOG_FOLDER, LOG_FILENAME),
            'formatter': 'verbose',
            'maxBytes':604800, 
            'backupCount':50
            }
        },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers':['file', 'mail_admins',],
            'propagate': True,
            'level':'INFO',
            },
        'django.schema': {
            'handlers':['file', 'mail_admins',],
            'propagate': True,
            'level':'INFO',
            },
        'django.db': {
            'handlers': ['file','mail_admins',],
            'propagate': True,
            'level': 'INFO'
        },
    }
    }

if os.path.exists(os.path.join(PROJECT_HOME,"local_settings.py")):
    from local_settings import *


#################
#
# DON'T PUT ANY MORE SETTINGS AFTER THIS POINT, OTHERWISE local_settings.py CAN'T OVERRIDE THEM
#
#
    
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(LOG_FOLDER, "cephia.db")
        }
    }
        
#check that required settings are set
if DATABASES['default']['ENGINE'] == 'django.db.backends.':
    raise Exception("Unconfigured databases setting, please correct in local_settings.py")

DATABASES['default']['ATOMIC_REQUESTS'] = True
