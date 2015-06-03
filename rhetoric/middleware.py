import json
from django.http import HttpResponse, HttpRequest
from django.middleware.csrf import CsrfViewMiddleware

from .view import ViewCallback
from .compat import text_


def json_body_getter(request_instance):
    if hasattr(request_instance, '_json_body'):
        return request_instance._json_body
    json_body = json.loads(text_(request_instance.read(), request_instance.encoding or 'utf-8'))
    setattr(request_instance, '_json_body', json_body)
    return json_body


class CsrfProtectedViewDispatchMiddleware(CsrfViewMiddleware):

    def __init__(self):
        super(CsrfProtectedViewDispatchMiddleware, self).__init__()
        self.add_property(HttpRequest, 'json_body', json_body_getter)

    def process_request(self, request):
        # We assume here that CsrfViewMiddleware doesn't have the process_request method
        # which should be called via super().
        # -------------------------------------------------
        # set request.response object as in
        # http://docs.pylonsproject.org/projects/pyramid/en/latest/api/request.html#pyramid.request.Request.response
        setattr(request, 'response', HttpResponse())


    def process_view(self, request, callback, callback_args, callback_kwargs):
        if isinstance(callback, ViewCallback):
            view_settings = callback.find_view_settings(request, callback_args, callback_kwargs)
            # Check the actual view callable rather than ViewCallback wrapper with CsrfViewMiddleware
            return super(CsrfProtectedViewDispatchMiddleware, self).process_view(
                request, view_settings['view'], callback_args, callback_kwargs
            )

        # The callable is a regular django view
        return super(CsrfProtectedViewDispatchMiddleware, self).process_view(
            request, callback, callback_args, callback_kwargs
        )

    def add_property(self, cls, name, method):
        if not hasattr(cls, name):
            setattr(cls, name, property(method))