"""Local development defaults. Use studyhub.production for deployment checks."""
from pathlib import Path
import os
from django.utils.csp import CSP
BASE_DIR=Path(__file__).resolve().parent.parent
SECRET_KEY=os.environ.get('DJANGO_SECRET_KEY','development-only-change-this-before-production-61-studyhub')
DEBUG=True
ALLOWED_HOSTS=['localhost','127.0.0.1','testserver']
INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','rest_framework','desk']
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csp.ContentSecurityPolicyMiddleware','desk.middleware.RequestIDMiddleware']
ROOT_URLCONF='studyhub.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates'], 'APP_DIRS':True,
    'OPTIONS':{'context_processors':['django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION='studyhub.wsgi.application';ASGI_APPLICATION='studyhub.asgi.application'
DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'db.sqlite3'}}
AUTH_USER_MODEL='desk.User'
AUTH_PASSWORD_VALIDATORS=[{'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator','OPTIONS':{'min_length':10}},
    {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LANGUAGE_CODE='zh-hant';TIME_ZONE='Asia/Taipei';USE_I18N=True;USE_TZ=True
STATIC_URL='/static/';STATIC_ROOT=BASE_DIR/'staticfiles'
STORAGES={'default':{'BACKEND':'django.core.files.storage.FileSystemStorage'},
          'staticfiles':{'BACKEND':'django.contrib.staticfiles.storage.StaticFilesStorage'}}
MEDIA_ROOT=BASE_DIR/'private-media'  # Intentionally no public MEDIA_URL route.
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
LOGIN_URL='login';LOGIN_REDIRECT_URL='desk:list';LOGOUT_REDIRECT_URL='login'
EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend';DEFAULT_FROM_EMAIL='studyhub@example.invalid'
CACHES={'default':{'BACKEND':'django.core.cache.backends.locmem.LocMemCache','LOCATION':'studyhub-local'}}
TASKS={'default':{'BACKEND':'django.tasks.backends.immediate.ImmediateBackend'}}
SECURE_CSP={'default-src':[CSP.SELF],'object-src':[CSP.NONE],'base-uri':[CSP.SELF],'frame-ancestors':[CSP.NONE]}
DATA_UPLOAD_MAX_MEMORY_SIZE=128*1024;FILE_UPLOAD_MAX_MEMORY_SIZE=64*1024
REST_FRAMEWORK={'DEFAULT_AUTHENTICATION_CLASSES':['rest_framework.authentication.SessionAuthentication'],
    'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination','PAGE_SIZE':5}
