import unittest
import os


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.testapp.testapp.settings")

        from django.test.client import Client
        import rhetoric

        self.client = Client()
        self.rhetoric = rhetoric