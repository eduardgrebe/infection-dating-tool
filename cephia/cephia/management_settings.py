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
            'handlers': ['file', 'mail_admins'],
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
    


