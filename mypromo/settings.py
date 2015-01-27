"""
Django settings for mypromo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k+at_(cnuwar=vkpj724auc6c3jea+gpr&@f(7z0zi#%p08l+9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #Apps proyecto
    'userprofiles',
    'mypromo',
    'cupones',
    'promociones',
    'sorl.thumbnail',
    'rest_framework',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY': 10
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ATOMIC_REQUESTS': True,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es-MX'

TIME_ZONE = 'America/Merida'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = '/Users/jonathan/www/mypromo.com/media'

MEDIA_URL = '/media/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder',
 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
#STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'))

# Email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'jepc1491@gmail.com'
EMAIL_HOST_PASSWORD = 'vv1_barcelona'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
