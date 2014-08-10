"""Django settings for my_django project."""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# set variable for development / production settings
import socket
SERVER = socket.gethostname()
DEV_SERV = ('r40',); RHC_SERV = ('ex-std-node157.prod.rhcloud.com',)
ON_DEV_SERV = False; ON_RHC_SERV = False
if SERVER in DEV_SERV:
    ON_DEV_SERV = True
elif SERVER in RHC_SERV:
    ON_RHC_SERV = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'eghs4my-dqs!pkzmm!#0k%%)^l-u-(sklrm_l(qgado19xx=-7'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.webdesign',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'my_django.urls'

WSGI_APPLICATION = 'my_django.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'

if ON_DEV_SERV:

    DEBUG = True

    TEMPLATE_DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'var/db.sqlite3'),
        }
    }

    INSTALLED_APPS += (
        'debug_toolbar',
    )

    # debug_toolbar settings
    DEBUG_TOOLBAR_PATCH_SETTINGS = False

    INTERNAL_IPS = ('127.0.0.1',)

    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

elif ON_RHC_SERV:
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    TEMPLATE_DEBUG = False

    ALLOWED_HOSTS = [os.environ['OPENSHIFT_GEAR_DNS'],]

    if os.environ.has_key('OPENSHIFT_POSTGRESQL_DB_HOST'):
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': os.environ.get('OPENSHIFT_APP_NAME'),
                'USER': os.environ.get('OPENSHIFT_POSTGRESQL_DB_USERNAME'),
                'PASSWORD': os.environ.get('OPENSHIFT_POSTGRESQL_DB_PASSWORD'),
                'HOST': os.environ.get('OPENSHIFT_POSTGRESQL_DB_HOST'),
                'PORT': os.environ.get('OPENSHIFT_POSTGRESQL_DB_PORT'),
            }
        }
    elif os.environ.has_key('OPENSHIFT_MYSQL_DB_HOST'):
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ.get('OPENSHIFT_APP_NAME'),
                'USER': os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME'),
                'PASSWORD': os.environ.get('OPENSHIFT_MYSQL_DB_PASSWORD'),
                'HOST': os.environ.get('OPENSHIFT_MYSQL_DB_HOST'),
                'PORT': os.environ.get('OPENSHIFT_MYSQL_DB_PORT'),
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', BASE_DIR), 'db.sqlite3'),
            }
        }

    STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', BASE_DIR), 'static/static/')

    MEDIA_ROOT = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', BASE_DIR), 'static/media/')

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(os.environ['OPENSHIFT_DIY_LOG_DIR'], 'my_django.log'),
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    }

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': ':'.join([os.environ.get('OPENSHIFT_INTERNAL_IP', '127.0.0.1'), '18080']),
        }
    }
