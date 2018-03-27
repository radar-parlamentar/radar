"""Django settings for radar_parlamentar project."""
import os
from pathlib import Path

ADMINS = (('Leonardo', 'leonardofl87@gmail.com'),
          ('Diego', 'diraol@diraol.eng.br'))
MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/radar/radar_parlamentar/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/radar/radar_parlamentar/radar_parlamentar/static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.getenv('RADAR_SECRET_KEY',
                       '&amp;bt*nmd1d(+8*rm^nm9#0ge$iepd8!vw(#v9+z3!e9iel^ls8')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            Path('radar_parlamentar/templates/').resolve(),
        ],
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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'radar_parlamentar.middleware.ExceptionLoggingMiddleware'
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'radar_parlamentar.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'radar_parlamentar.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cron',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'modelagem',
    'importadores',
    'analises',
    'exportadores',
    'testes_integracao',
    'radar_parlamentar',
    'plenaria',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(levelname)s %(asctime)s %(module)s %(process)d '
                       '%(thread)d %(message)s')
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'filename': 'radar.log',
            'backupCount': 2,
            'maxBytes': 1024*1024*10,  # 10MB
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'radar': {
            'handlers': ['file'],
            'level': 'DEBUG',
            # 'propagate': True,
        }
    }
}

ELASTIC_SEARCH_ADDRESS = {'host': 'elasticsearch', 'port': '9200'}
ELASTIC_SEARCH_INDEX = "radar_parlamentar"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'radar',
        'USER': 'radar',
        'PASSWORD': os.getenv('RADAR_DB_PASSWORD', 'radar'),
        'HOST': 'postgres'
    }
}

ALLOWED_HOSTS = ['radarparlamentar.polignu.org', 'localhost']

CELERY_BROKER_URL= 'amqp://guest:guest@rabbitmq:5672//'

DEBUG = True

LOGGING['handlers']['file']['filename'] = '/var/log/radar/radar.log'

if os.getenv('RADAR_IS_PRODUCTION'):

    print('Starting PRODUCTION environment ...')

    DEBUG = False

    # First one on the list
    MIDDLEWARE.insert(0, 'django.middleware.cache.UpdateCacheMiddleware')
    # Last one on the list
    MIDDLEWARE.append('django.middleware.cache.FetchFromCacheMiddleware')

    # Timeout here is the time that the django-server will hold the cached
    # files on the server, it is not directly related to the http headers
    # timeout information (defined below).
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': 'memcache:11211',
            'TIMEOUT': 60*60*48
        }
    }

    # The number of seconds each page should be cached
    # https://docs.djangoproject.com/en/2.0/topics/cache/#the-per-site-cache
    CACHE_MIDDLEWARE_SECONDS = 60*60

    CRON_CLASSES  = [
        'cron.jobs.DemoJob',
    ]

if os.getenv('RADAR_TEST'):
    print('Starting TEST environment ...')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'radar_parlamentar.db',
        }
        # 'default': {
        #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #     'NAME': 'radar',
        #     'USER': 'radar',
        #     'PASSWORD': 'radar',
        #     'HOST': 'test_db'
        # }
    }

TEMPLATE_DEBUG = DEBUG
