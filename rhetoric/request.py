""" Request-related shortcuts.
"""
import json

from django.utils.functional import SimpleLazyObject

from .compat import text_


class JsonBodyProperty(SimpleLazyObject):
    def __init__(self, request):
        super(JsonBodyProperty, self).__init__(lambda: json.loads(text_(request.read(), request.encoding or 'utf-8')))
