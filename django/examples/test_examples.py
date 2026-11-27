"""Run with Python unittest OR manage.py test; no database server required."""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','studyhub.testing')
import django
django.setup()
from django.test.utils import setup_test_environment
from demo_core import initialize
initialize();setup_test_environment()
from desk.tests import StudyHubTests

if __name__=='__main__':
    import unittest
    unittest.main()
