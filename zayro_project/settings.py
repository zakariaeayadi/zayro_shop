import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-k9tgz68e2f&zn8m&*24e-=52we_($!@!!z%*z=9&n%2i4@d+%g'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition
INSTALLED_APPS = [
    'sslserver',
    'unfold',  # Must be first
    'unfold.contrib.filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Required by allauth

    # --- ALLAUTH APPS ---
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

    # Custom Apps
    'store',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <-- هادي
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Allauth Middleware
    'allauth.account.middleware.AccountMiddleware',
]
ALLOWED_HOSTS = ['*'] # أو حط '.onrender.com'

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
ROOT_URLCONF = 'zayro_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'zayro_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files & Media
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================================
# ALLAUTH & SOCIAL AUTHENTICATION CONFIGURATION
# ==============================================================================

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Redirections
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Account settings
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Social Account settings
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_REQUIRED = False

# Social Providers setup
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['public_profile', 'email'],
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'name',
            'picture',
        ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
        'VERSION': 'v19.0',
    }
}

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'zayroshop05@gmail.com'
EMAIL_HOST_PASSWORD = 'vylg rhwx lttl uoyr'  # Remplacer par App Password d-Google
DEFAULT_FROM_EMAIL = 'ZAYRO <zayroshop05@gmail.com>'

# Ila knti ba9i f le Mode Developpement (Local) w bghiti t-testi l-emails f terminal, de-commenter had la ligne:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'