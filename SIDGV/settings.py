# Django settings for Userena SIDGV project.
# -*- encoding: utf-8 -*-
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

import os

settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))

ADMINS = (
    ('mricharleon', 'mricharleon@gmail.com'),
)


MANAGERS = ADMINS

DATABASES = {
    'default': {
        
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Internationalization
TIME_ZONE = 'America/Guayaquil'
LANGUAGE_CODE = 'es-EC'
ugettext = lambda s: s
LANGUAGES = (
    ('en', ugettext('English')),
    ('nl', ugettext('Dutch')),
    ('fr', ugettext('French')),
    ('pl', ugettext('Polish')),
    ('pt', ugettext('Portugese')),
    ('pt-br', ugettext('Brazilian Portuguese')),
    ('es', ugettext('Spanish')),
    ('el', ugettext('Greek')),
)
LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, 'locale'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'public/media/')
MEDIA_URL = '/media/'
#STATIC_ROOT = os.path.join(PROJECT_ROOT, '/static/')

STATIC_ROOT = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2] + ['static'])
STATIC_URL = '/static/'

#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'SIDGV/static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
#SECRET_KEY = '_g-js)o8z#8=9pr1&amp;05h^1_#)91sbo-)g^(*=-+epxmt4kc9m#'
SECRET_KEY = '#bfph1+o@5_#+sfv##*@5m@pgc9cx6_(hcx@o#hlw!t&i-@gc7'
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'ssl_redirect.middleware.SSLRedirectMiddleware',
    # para la seguridad de django secure
    #'djangosecure.middleware.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'drealtime.middleware.iShoutCookieMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'userena.middleware.UserenaLocaleMiddleware',
)

# Add the Guardian and userena authentication backends
AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Settings used by Userena
LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'
AUTH_PROFILE_MODULE = 'profiles.Profile'
USERENA_DISABLE_PROFILE_LIST = True
USERENA_MUGSHOT_SIZE = 140



ROOT_URLCONF = 'SIDGV.urls'
WSGI_APPLICATION = 'SIDGV.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'SIDGV/templates/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    #'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'guardian',
    'south',
    'userena',
    #'userena.contrib.umessages',
    'profiles',
    'easy_thumbnails',
    'ganados',
    'alimentos',
    'notifications',
    'reports',
    #'webServices.wsGanados',
    'drealtime', 
    'messages',
    'medicament',
    'mockups',
    'django_extensions',
    'djangosecure',
    'django_cron',
)

# django realtime
ISHOUT_CLIENT_ADDR = '192.168.1.2:5500'
ISHOUT_API_ADDR = '127.0.0.1:6600'
ISHOUT_HTTPS = True


CRON_CLASSES = [
    "ganados.cron.CronJobProduccion",
    "django_cron.cron.FailedRunsNotificationCronJob",
    # ...
]
#ALLOW_PARALLEL_RUNS = True
#CRON_CACHE = 'cron_cache'

USE_TLS = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SSL_DOMAIN = 'https://192.168.1.2:1290'
SSL_SECTIONS = (
    '/list_cattle',
    '/agrega_ganaderia_config',
    '/agrega_ganado_ordenio',
    '/list_cattle_male',
    '/lista_ganado_produccion',
    '/list_insemination',
    '/list_food',
    '/list_wormer',
    '/list_vaccine',
    '/accounts',
    '/add_attempt_service',
    '/admin',
    '/messages',
)



# django xtension

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True

CRSF_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE=True




# para graficar la BD

GRAPH_MODELS={'all_applications':True,
                'group_models':True,
            }


SOUTH_MIGRATION_MODULES = {
        'easy_thumbnails': 'easy_thumbnails.south_migrations',
    }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Needed for Django guardian
ANONYMOUS_USER_ID = -1

# Test runner
TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'

#correo
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
