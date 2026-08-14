import os
from pathlib import Path
from decouple import config
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ========================================
# SECURITY & ENVIRONMENT
# ========================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

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
# CLOUDINARY CONFIGURATION
# ========================================

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default='dnbjcrqml'),
    'API_KEY': config('CLOUDINARY_API_KEY', default='682674164735159'),
    'API_SECRET': config('CLOUDINARY_API_SECRET', default='f8JG-PTwseB9pccYqrIjarDu_Lw'),
}

# Initialize Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET']
)

# Use Cloudinary for all media file uploads
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Cloudinary upload options
CLOUDINARY_UPLOAD_OPTIONS = {
    'folder': 'elvis_portfolio',
    'use_filename': True,
    'unique_filename': True,
    'overwrite': False,
    'resource_type': 'auto',
}

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
                'apps.core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ========================================
# DATABASE
# ========================================

# Use DATABASE_URL from environment or fallback to SQLite
DATABASE_URL = config('DATABASE_URL', default='sqlite:///db.sqlite3')

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}

# ========================================
# PASSWORD VALIDATION
# ========================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ========================================
# INTERNATIONALIZATION
# ========================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ========================================
# STATIC & MEDIA FILES
# ========================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files are now handled by Cloudinary
# But keep these for local development fallback
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

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

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

if not DEBUG:
    EMAIL_HOST = config('EMAIL_HOST', default='')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@example.com')

# ========================================
# SITE SETTINGS
# ========================================

SITE_NAME = config('SITE_NAME', default='Elvis T. Harmon - Software Engineer')
SITE_TAGLINE = config('SITE_TAGLINE', default='Building Intelligent Software That Solves Real Problems')
ADMIN_EMAIL = config('ADMIN_EMAIL', default='harmonelvis78@gmail.com')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='harmonelvis78@gmail.com')

# ========================================
# ANALYTICS
# ========================================

ANALYTICS_GENERATE_SAMPLE_DATA = config('ANALYTICS_GENERATE_SAMPLE_DATA', default=False, cast=bool)

# ========================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ========================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========================================
# SECURITY (Production)
# ========================================

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ========================================
# FORCE CLOUDINARY STORAGE (OVERRIDE)
# ========================================

# This forces Cloudinary as the default storage
# It overrides any other storage settings
import django.core.files.storage
from cloudinary_storage.storage import MediaCloudinaryStorage

# Override the default storage
django.core.files.storage.default_storage = MediaCloudinaryStorage()

# Also update the global storage instance
from django.core.files.storage import default_storage
# Re-assign to ensure it takes effect
default_storage = MediaCloudinaryStorage()

print("✅ Cloudinary storage forced as default!")

# ========================================
# VERIFICATION (Optional - Remove in Production)
# ========================================

if DEBUG:
    print(f"🔍 Cloudinary Cloud Name: {CLOUDINARY_STORAGE['CLOUD_NAME']}")
    print(f"🔍 Default Storage: {DEFAULT_FILE_STORAGE}")
    print("✅ Cloudinary configured successfully!")