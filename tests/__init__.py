import unittest
import os
import re


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.testapp.testapp.settings")

        from django.test.client import Client
        from tests.testapp.testapp.wsgi import application
        import rhetoric


        DEFAULT_HEADERS = {
            'X-API-VERSION': '1.0'
        }
        self.client = Client(**DEFAULT_HEADERS)
        self.rhetoric = rhetoric
        self.wsgi_app = application
