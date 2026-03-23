from settings import *

import os
PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))

LOG_FOLDER = os.path.join(PROJECT_HOME, "..", "..", 'logs')

if os.path.exists(os.path.join(PROJECT_HOME,"local_settings.py")):
    from local_settings import *

LOG_LEVEL="DEBUG"
LOG_FILENAME="cephia_management.log"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(process)d %(filename)s %(lineno)d: %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
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
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
         'console': {
             'level': 'INFO',
             'class': 'logging.StreamHandler',
             'filters': ['require_debug_true'],
             'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console', 'mail_admins'],
            'propagate': True,
            'level': 'ERROR'
        },
        'django': {
            'handlers': ['file', 'console', 'mail_admins'],
            'propagate': True,
            'level': 'ERROR'
        },
    },
}
