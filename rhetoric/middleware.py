from django.http import HttpResponse
from django.middleware.csrf import CsrfViewMiddleware

from rhetoric.view import ViewCallback
from rhetoric.request import JsonBodyProperty


class CsrfProtectedViewDispatchMiddleware(CsrfViewMiddleware):

    def process_request(self, request):
        # We assume here that CsrfViewMiddleware doesn't have the process_request method
        # which should be called via super().
        # -------------------------------------------------
        # set request.response object as in
        # http://docs.pylonsproject.org/projects/pyramid/en/latest/api/request.html#pyramid.request.Request.response
        setattr(request, 'response', HttpResponse())
        setattr(request, 'json_body', JsonBodyProperty(request))


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
