"""Deployment template. No live service or PostgreSQL is provisioned by this file."""
from .settings import *
from django.core.exceptions import ImproperlyConfigured
SECRET_KEY=os.environ.get('DJANGO_SECRET_KEY','')
if len(SECRET_KEY)<50 or len(set(SECRET_KEY))<8:raise ImproperlyConfigured('Set a strong DJANGO_SECRET_KEY in the runtime environment')
DEBUG=False
ALLOWED_HOSTS=[x.strip() for x in os.environ.get('DJANGO_ALLOWED_HOSTS','').split(',') if x.strip()]
if not ALLOWED_HOSTS:raise ImproperlyConfigured('Set explicit DJANGO_ALLOWED_HOSTS')
SECURE_SSL_REDIRECT=True;SESSION_COOKIE_SECURE=True;CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=3600;SECURE_HSTS_INCLUDE_SUBDOMAINS=False;SECURE_HSTS_PRELOAD=False
SECURE_CONTENT_TYPE_NOSNIFF=True;X_FRAME_OPTIONS='DENY'
STORAGES={**STORAGES,'staticfiles':{'BACKEND':'whitenoise.storage.CompressedManifestStaticFilesStorage'}}
if os.environ.get('POSTGRES_DB'):
    DATABASES={'default':{'ENGINE':'django.db.backends.postgresql','NAME':os.environ['POSTGRES_DB'],
        'USER':os.environ['POSTGRES_USER'],'PASSWORD':os.environ['POSTGRES_PASSWORD'],
        'HOST':os.environ['POSTGRES_HOST'],'PORT':os.environ.get('POSTGRES_PORT','5432'),
        'CONN_MAX_AGE':60,'OPTIONS':{'sslmode':os.environ.get('POSTGRES_SSLMODE','require')}}}
# Do not blindly trust forwarded headers. Configure the known reverse proxy separately.
