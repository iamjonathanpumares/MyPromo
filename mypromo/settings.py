"""
Django settings for mypromo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from __future__ import absolute_import
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k+at_(cnuwar=vkpj724auc6c3jea+gpr&@f(7z0zi#%p08l+9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'sorl.thumbnail',
    'rest_framework',
    'password_reset',
    'djcelery',
    'corsheaders',
    'rest_framework.authtoken',
)

LOCAL_APPS = (
    'userprofiles',
    'mypromo',
    'cupones',
    'promociones',
    'paquetes',
    'locales',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
    #'PAGINATE_BY': 10
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'async_messages.middleware.AsyncMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "userprofiles.context_processors.datos_afiliado",
)

ROOT_URLCONF = 'mypromo.urls'

WSGI_APPLICATION = 'mypromo.wsgi.application'

#AUTH_USER_MODEL = 'userprofiles.UsuarioPromotor'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'progogi',
        'USER': 'jepumares',
        'password': 'progogi_postgresql',
        'HOST': 'localhost'
    }
}

# AUTHENTICATION BACKENDS
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'userprofiles.backends.EmailBackend',
)

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Configuration CORS Headers
CORS_ORIGIN_ALLOW_ALL = True

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es-MX'

TIME_ZONE = 'America/Merida'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#MEDIA_ROOT = '/Users/jonathan/www/mypromo.com/media'

#MEDIA_URL = '/media/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder',
 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
#STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'))

# Email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'veltiumdevelopment@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# CELERY SETTINGS
BROKER_URL = 'amqp://jepumares:12345@jonathan-P43G:5672/mypromovhost'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Usar la base de datos Django ORM para guardar los resultados de las tareas de Celery (Backend de resultados)
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

# CACHE SETTINGS
"""CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}"""

# Periodic Tasks
#from datetime import timedelta
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'cambiar-status': {
        'task': 'userprofiles.tasks.cambiarStatus',
        'schedule': crontab(minute=42, hour=18)
    },
}

#CELERY_TIMEZONE = 'UTC'
