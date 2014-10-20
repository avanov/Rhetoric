"""
WSGI config for testapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os
import re


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testapp.settings")
# We must explicitly setup django here (starting from Django 1.7)
import django
if django.VERSION[:2] >= (1, 7):
    django.setup()

from .rhetoric_config import config

config.scan(
    ignore=[
    # do not scan settings modules
    re.compile('^testapp.testapp.settings[_]?[_a-z09]*$').match,
])

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
