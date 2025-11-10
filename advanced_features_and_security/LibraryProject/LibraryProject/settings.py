"""
Django settings for LibraryProject with enhanced security configurations.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
# Security: DEBUG set to False for production, can be overridden by environment variable
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'

# Security: Define allowed hosts for production security
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.yourdomain.com',  # Replace with your actual domain in production
]

# Security: Additional allowed hosts from environment
if os.environ.get('DJANGO_ALLOWED_HOSTS'):
    ALLOWED_HOSTS.extend(os.environ.get('DJANGO_ALLOWED_HOSTS').split(','))

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party security apps
    'csp',  # Content Security Policy
    # Local apps
    'bookshelf',
]

MIDDLEWARE = [
    # Security: Content Security Policy middleware (Step 4)
    'csp.middleware.CSPMiddleware',
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'LibraryProject.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# ==================== SECURITY SETTINGS ====================

# Security: HTTPS Settings (Step 1)
if not DEBUG:
    SECURE_SSL_REDIRECT = True  # Redirect all HTTP to HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Security: Cookie Settings (Step 1)
SESSION_COOKIE_SECURE = not DEBUG  # Send session cookies over HTTPS only
CSRF_COOKIE_SECURE = not DEBUG     # Send CSRF cookies over HTTPS only
SESSION_COOKIE_HTTPONLY = True     # Prevent JavaScript access to session cookie
CSRF_COOKIE_HTTPONLY = False       # Allow JavaScript to read CSRF token (needed for AJAX)
SESSION_COOKIE_SAMESITE = 'Lax'    # CSRF protection
CSRF_COOKIE_SAMESITE = 'Lax'

# Security: Browser Protection Headers (Step 1)
SECURE_BROWSER_XSS_FILTER = True   # Enable XSS filter in browsers
X_FRAME_OPTIONS = 'DENY'           # Prevent clickjacking
SECURE_CONTENT_TYPE_NOSNIFF = True # Prevent MIME type sniffing

# Security: HSTS Settings (only in production)
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Security: Content Security Policy (CSP) - Step 4
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)  # Only allow scripts from same origin
CSP_STYLE_SRC = ("'self'",)   # Only allow styles from same origin
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'",)
CSP_OBJECT_SRC = ("'none'",)  # No Flash/Java applets
CSP_BASE_URI = ("'self'",)
CSP_FORM_ACTION = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)  # Equivalent to X-Frame-Options: DENY

# Security: Additional headers
SECURE_REFERRER_POLICY = 'same-origin'

# Security: File upload restrictions
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000    # Prevent memory exhaustion attacks

# Security: Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Security: Logging for security events
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'security.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
