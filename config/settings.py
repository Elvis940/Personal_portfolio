import os
from pathlib import Path
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-your-secret-key-here')
DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='localhost,127.0.0.1,.onrender.com').split(',')

# ========================================
# DATABASE
# ========================================
# Use DATABASE_URL from environment or fallback to SQLite
DATABASE_URL = config('DATABASE_URL', default='sqlite:///db.sqlite3')

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}
# ========================================
# APPLICATION DEFINITION
# ========================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'crispy_forms',
    'crispy_bootstrap5',
    'ckeditor',
    'cloudinary',
    'cloudinary_storage',
    
    # Local apps
    'apps.core',
    'apps.profiles',
    'apps.projects',
    'apps.blog',
    'apps.services',
    'apps.testimonials',
    'apps.contact',
    'apps.github',
    'apps.analytics',
    'apps.ai_assistant',
    'apps.dashboard',
]

# ========================================
# MIDDLEWARE
# ========================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ========================================
# TEMPLATES
# ========================================

ROOT_URLCONF = 'config.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ========================================
# STATIC & MEDIA FILES
# ========================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ========================================
# CLOUDINARY CONFIGURATION
# ========================================

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default=''),
    'API_KEY': config('CLOUDINARY_API_KEY', default=''),
    'API_SECRET': config('CLOUDINARY_API_SECRET', default=''),
}

# Initialize Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET']
)

# Cloudinary upload options
CLOUDINARY_UPLOAD_OPTIONS = {
    'folder': 'elvis_portfolio',
    'use_filename': True,
    'unique_filename': True,
    'overwrite': False,
    'resource_type': 'auto',
}

# ========================================
# CRISPY FORMS
# ========================================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ========================================
# CKEDITOR
# ========================================

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}

# ========================================
# EMAIL CONFIGURATION
# ========================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ========================================
# SITE SETTINGS
# ========================================


SITE_NAME = config('SITE_NAME', default='Elvis T. Harmon - Software Engineer')
SITE_TAGLINE = config('SITE_TAGLINE', default='Building Intelligent Software That Solves Real Problems')
ADMIN_EMAIL = config('ADMIN_EMAIL', default='harmonelvis78@gmail.com')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='harmonelvis78@gmail.com')


EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

if not DEBUG:
    EMAIL_HOST = config('EMAIL_HOST', default='')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@example.com')


# ========================================
# ANALYTICS
# ========================================

ANALYTICS_GENERATE_SAMPLE_DATA = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
