from .settings import *
DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':':memory:'}}
PASSWORD_HASHERS=['django.contrib.auth.hashers.MD5PasswordHasher']  # Test speed ONLY.
EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
STORAGES={'default':{'BACKEND':'django.core.files.storage.InMemoryStorage'},
          'staticfiles':{'BACKEND':'django.contrib.staticfiles.storage.StaticFilesStorage'}}
LOGGING={'version':1,'disable_existing_loggers':False,'handlers':{'null':{'class':'logging.NullHandler'}},
         'loggers':{'django.request':{'handlers':['null'],'propagate':False}}}
